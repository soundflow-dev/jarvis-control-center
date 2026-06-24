from __future__ import annotations

import json
from typing import Any

from cryptography.fernet import Fernet, InvalidToken

from app.config import settings


fernet = Fernet(settings.fernet_key)


def encrypt_json(payload: dict[str, Any] | None) -> str | None:
    if not payload:
        return None
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return fernet.encrypt(raw).decode("utf-8")


def decrypt_json(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    try:
        return json.loads(fernet.decrypt(value.encode("utf-8")).decode("utf-8"))
    except InvalidToken as exc:
        raise ValueError("Device credentials cannot be decrypted. Check APP_SECRET_KEY.") from exc
