from __future__ import annotations

from fastapi import APIRouter


router = APIRouter(prefix="/api/transfers", tags=["transfers"])


@router.get("/policy")
def transfer_policy():
    return {
        "name": "Transfers that just work",
        "defaults": [
            "copy file contents",
            "preserve basic timestamps when possible",
            "preserve basic permissions when safe",
            "ignore incompatible xattrs and ACLs",
            "never fail because of Apple metadata streams",
        ],
    }
