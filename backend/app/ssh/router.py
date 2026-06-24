from __future__ import annotations

from fastapi import APIRouter


router = APIRouter(prefix="/api/ssh", tags=["ssh"])


@router.get("/capabilities")
def capabilities():
    return {"terminal": "planned", "transport": "backend-mediated SSH over WebSocket"}
