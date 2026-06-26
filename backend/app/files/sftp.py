from __future__ import annotations

import io
import posixpath
import stat
from datetime import datetime
from urllib.parse import urlparse

from fastapi import HTTPException, status

from app.database.models import Device
from app.devices.service import connect_ssh_device


def normalize_path(path: str | None) -> str:
    if not path:
        return "."
    normalized = posixpath.normpath(path)
    return "." if normalized in ("", ".") else normalized


def parent_path(path: str) -> str:
    if path in ("", ".", "/"):
        return "."
    parent = posixpath.dirname(path.rstrip("/"))
    return parent or "."


def configured_start_path(device: Device) -> str | None:
    if not device.connection_url:
        return None
    parsed = urlparse(device.connection_url)
    if parsed.scheme not in ("sftp", "ssh"):
        return None
    if not parsed.path or parsed.path == "/":
        return None
    return normalize_path(parsed.path)


def initial_path_candidates(device: Device, sftp) -> list[str]:
    candidates: list[str] = []
    configured = configured_start_path(device)
    if configured:
        candidates.append(configured)
    candidates.append(".")
    try:
        current = sftp.getcwd()
        if current:
            candidates.append(normalize_path(current))
    except OSError:
        pass
    candidates.extend(["/", "/config", "/homeassistant"])
    return list(dict.fromkeys(candidates))


def sftp_for_device(device: Device):
    if device.connection_type != "ssh_sftp":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File explorer is currently available for SFTP devices.")
    client = connect_ssh_device(device)
    return client, client.open_sftp()


def entry_from_attr(path: str, attr) -> dict:
    is_dir = stat.S_ISDIR(attr.st_mode)
    return {
        "name": attr.filename,
        "path": posixpath.join(path, attr.filename) if path not in ("", ".") else attr.filename,
        "type": "directory" if is_dir else "file",
        "size": attr.st_size,
        "modified_at": datetime.fromtimestamp(attr.st_mtime).isoformat() if attr.st_mtime else None,
        "permissions": stat.filemode(attr.st_mode),
    }


def list_sftp_directory(device: Device, path: str | None) -> dict:
    safe_path = normalize_path(path)
    client, sftp = sftp_for_device(device)
    try:
        if safe_path == ".":
            entries = None
            errors: list[str] = []
            for candidate in initial_path_candidates(device, sftp):
                try:
                    entries = [entry_from_attr(candidate, attr) for attr in sftp.listdir_attr(candidate)]
                    safe_path = candidate
                    break
                except OSError as exc:
                    errors.append(f"{candidate}: {exc}")
            if entries is None:
                detail = "SFTP initial directory is not available."
                if errors:
                    detail += " Tried " + "; ".join(errors)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
        else:
            entries = [entry_from_attr(safe_path, attr) for attr in sftp.listdir_attr(safe_path)]
        entries.sort(key=lambda item: (item["type"] != "directory", item["name"].lower()))
        return {"path": safe_path, "parent": parent_path(safe_path), "entries": entries}
    finally:
        sftp.close()
        client.close()


def make_sftp_directory(device: Device, path: str) -> None:
    client, sftp = sftp_for_device(device)
    try:
        sftp.mkdir(normalize_path(path))
    finally:
        sftp.close()
        client.close()


def delete_sftp_path(device: Device, path: str) -> None:
    safe_path = normalize_path(path)
    if safe_path in ("", ".", "/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refusing to delete the root folder.")
    client, sftp = sftp_for_device(device)
    try:
        delete_sftp_tree(sftp, safe_path)
    finally:
        sftp.close()
        client.close()


def delete_sftp_tree(sftp, path: str) -> None:
    attr = sftp.stat(path)
    if stat.S_ISDIR(attr.st_mode):
        for child in sftp.listdir_attr(path):
            delete_sftp_tree(sftp, posixpath.join(path, child.filename))
        sftp.rmdir(path)
        return
    sftp.remove(path)


def rename_sftp_path(device: Device, source: str, destination: str) -> None:
    client, sftp = sftp_for_device(device)
    try:
        sftp.rename(normalize_path(source), normalize_path(destination))
    finally:
        sftp.close()
        client.close()


def read_sftp_file(device: Device, path: str) -> tuple[str, io.BytesIO]:
    safe_path = normalize_path(path)
    client, sftp = sftp_for_device(device)
    try:
        with sftp.open(safe_path, "rb") as remote_file:
            content = remote_file.read()
        return posixpath.basename(safe_path), io.BytesIO(content)
    finally:
        sftp.close()
        client.close()
