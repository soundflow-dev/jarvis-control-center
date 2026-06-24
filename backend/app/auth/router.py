from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session as DbSession

from app.auth.schemas import LoginRequest, SetupRequest, SetupStatus, UserResponse
from app.auth.service import authenticate, create_initial_admin, create_session, get_current_user, logout, users_exist
from app.config import settings
from app.database.session import get_db


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/setup-status", response_model=SetupStatus)
def setup_status(db: DbSession = Depends(get_db)):
    warning = None
    if not settings.has_persistent_secret:
        warning = "APP_SECRET_KEY is not set. Configure it before production use."
    return SetupStatus(
        setup_required=not users_exist(db),
        secret_configured=settings.has_persistent_secret,
        warning=warning,
    )


@router.post("/setup", response_model=UserResponse)
def setup(payload: SetupRequest, response: Response, db: DbSession = Depends(get_db)):
    user = create_initial_admin(db, payload)
    create_session(db, user, response)
    return user


@router.post("/login", response_model=UserResponse)
def login(payload: LoginRequest, response: Response, db: DbSession = Depends(get_db)):
    user = authenticate(db, payload.identifier, payload.password)
    create_session(db, user, response)
    return user


@router.post("/logout")
def logout_route(request: Request, response: Response, db: DbSession = Depends(get_db)):
    logout(request, response, db)
    return {"ok": True}


@router.get("/me", response_model=UserResponse)
def me(request: Request, db: DbSession = Depends(get_db)):
    return get_current_user(request, db)
