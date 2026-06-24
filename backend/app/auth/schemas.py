from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class SetupStatus(BaseModel):
    setup_required: bool
    secret_configured: bool
    warning: str | None = None


class SetupRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr | None = None
    password: str = Field(min_length=10, max_length=256)
    confirm_password: str = Field(min_length=10, max_length=256)


class LoginRequest(BaseModel):
    identifier: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=256)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str | None
    is_admin: bool
    totp_enabled: bool

    model_config = {"from_attributes": True}
