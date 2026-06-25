from __future__ import annotations

import hashlib
import os
import posixpath
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from fastapi import HTTPException, status

from app.config import settings
from app.database.models import Device


NFS_MOUNT_ROOT = Path(os.getenv("NFS_MOUNT_ROOT", str(Path(settings.data_dir) / "nfs-mounts")))
NFS_MOUNT_OPTIONS = os.getenv("NFS_MOUNT_OPTIONS", "rw,nfsvers=4,soft,timeo=50,retrans=2").strip()


def _parse_nfs_url(device: Device) -> tuple[str, str]:
    value = (device.connection_url or "").strip()
    host = device.host
    export_path = "/"
    if value.startswith("nfs://"):
        parsed = urlparse(value)
        host = parsed.hostname or device.host
        export_path = parsed.path or "/"
    elif ":" in value:
        host_part, path_part = value.split(":", 1)
        host = host_part or device.host
        export_path = path_part or "/"
    elif value:
        host = value
    export_path = "/" + export_path.strip("/")
    return host, export_path


def _relative(path: str | None) -> str:
    if not path or path in (".", "/", "\\"):
        return "."
    normalized = posixpath.normpath(path.replace("\\", "/"))
    if normalized in ("", "/"):
        return "."
    if normalized.startswith("../") or normalized == "..":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid path.")
    return normalized.strip("/")


def _mount_id(host: str, export_path: str) -> str:
    return hashlib.sha256(f"{host}:{export_path}".encode("utf-8")).hexdigest()[:24]


def _is_mounted(target: Path) -> bool:
    try:
        mounts = Path("/proc/mounts").read_text(encoding="utf-8")
    except OSError:
        return False
    target_text = str(target)
    return any(line.split(" ")[1] == target_text for line in mounts.splitlines() if " " in line)


def mount_nfs_share(device: Device) -> Path:
    if device.connection_type != "nfs":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not an NFS share.")
    if not device.active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="NFS share is inactive.")
    host, export_path = _parse_nfs_url(device)
    mount_root = NFS_MOUNT_ROOT
    target = mount_root / _mount_id(host, export_path)
    target.mkdir(parents=True, exist_ok=True)
    if _is_mounted(target):
        return target

    command = ["mount", "-t", "nfs"]
    if NFS_MOUNT_OPTIONS:
        command.extend(["-o", NFS_MOUNT_OPTIONS])
    command.extend([f"{host}:{export_path}", str(target)])
    try:
        completed = subprocess.run(command, check=False, capture_output=True, text=True, timeout=20)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="NFS mount failed: mount command is not installed in the backend container.") from exc
    except subprocess.TimeoutExpired as exc:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=f"NFS mount timed out for {host}:{export_path}.") from exc
    if completed.returncode != 0:
        error = (completed.stderr or completed.stdout or "unknown mount error").strip()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"NFS mount failed for {host}:{export_path}: {error}. The backend container needs NFS mount permissions.",
        )
    return target


def _local_path(device: Device, path: str | None) -> Path:
    root = mount_nfs_share(device).resolve()
    relative = _relative(path)
    target = root if relative == "." else (root / relative).resolve()
    if target != root and root not in target.parents:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid path.")
    return target


def nfs_local_path(device: Device, path: str | None = None) -> Path:
    return _local_path(device, path)


def list_nfs_directory(device: Device, path: str | None) -> dict:
    current = _relative(path)
    root = _local_path(device, current)
    if not root.is_dir():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="NFS list failed: path is not a directory.")
    entries = []
    try:
        for entry in root.iterdir():
            stat_result = entry.stat()
            is_dir = entry.is_dir()
            entry_path = entry.name if current == "." else f"{current}/{entry.name}"
            entries.append(
                {
                    "name": entry.name,
                    "path": entry_path,
                    "type": "directory" if is_dir else "file",
                    "size": None if is_dir else stat_result.st_size,
                    "modified_at": datetime.fromtimestamp(stat_result.st_mtime).isoformat(),
                    "permissions": oct(stat_result.st_mode & 0o777),
                }
            )
    except OSError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"NFS list failed: {exc}") from exc
    entries.sort(key=lambda item: (item["type"] != "directory", item["name"].lower()))
    parent = "."
    if current != ".":
        parent_path = posixpath.dirname(current)
        parent = parent_path or "."
    return {"path": current, "parent": parent, "entries": entries}


def make_nfs_directory(device: Device, path: str) -> None:
    try:
        _local_path(device, path).mkdir(parents=True, exist_ok=False)
    except OSError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"NFS mkdir failed: {exc}") from exc


def delete_nfs_path(device: Device, path: str) -> None:
    relative = _relative(path)
    if relative == ".":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refusing to delete the NFS export root.")
    target = _local_path(device, relative)
    try:
        if target.is_dir() and not target.is_symlink():
            shutil.rmtree(target)
        else:
            target.unlink()
    except OSError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"NFS delete failed: {exc}") from exc


def rename_nfs_path(device: Device, source: str, destination: str) -> None:
    try:
        os.replace(_local_path(device, source), _local_path(device, destination))
    except OSError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"NFS rename failed: {exc}") from exc


def read_nfs_file(device: Device, path: str):
    target = _local_path(device, path)
    if not target.is_file():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="NFS download failed: path is not a file.")
    return target.name, target.open("rb")
