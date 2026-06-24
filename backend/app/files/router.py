from __future__ import annotations

from fastapi import APIRouter


router = APIRouter(prefix="/api/files", tags=["files"])


@router.get("/capabilities")
def capabilities():
    return {
        "sftp": ["list", "download", "upload"],
        "smb": [],
        "transfers": "MVP transfer endpoints will copy file contents and ignore incompatible xattrs/ACLs by design.",
    }
