from typing import AsyncGenerator, Annotated

from fastapi import Depends, HTTPException, status, Cookie, Header
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app import models, schemas
from backend.app.db import crud
from backend.app.core import security
from backend.app.core.config import settings
from backend.app.db.session import AsyncSessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

DBSession = Annotated[AsyncSession, Depends(get_db)]

async def get_current_user(
    session: DBSession,
    access_token: Annotated[str | None, Cookie()] = None
) -> models.User:
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt.decode(
            access_token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenData(email=payload.get("sub"))
    except (JWTError, schemas.ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    user = await crud.get_user_by_email(session, email=token_data.email)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

CurrentUser = Annotated[models.User, Depends(get_current_user)]

async def csrf_protect(
    csrf_token_cookie: Annotated[str | None, Cookie(alias="csrf_token")] = None,
    x_csrf_token_header: Annotated[str | None, Header(alias="x-csrf-token")] = None,
):
    """
    Dependency to protect against CSRF attacks using the double submit cookie pattern.
    It checks for the presence and validity of CSRF tokens in both the cookie and a request header.
    This dependency does not return a value; it only raises an exception if checks fail.
    """
    if not csrf_token_cookie or not x_csrf_token_header:
        raise HTTPException(status_code=403, detail="Missing CSRF token cookie or header")
    
    if csrf_token_cookie != x_csrf_token_header:
        raise HTTPException(status_code=403, detail="CSRF token mismatch")

    if not security.validate_csrf_token(csrf_token_cookie):
        raise HTTPException(status_code=403, detail="Invalid or expired CSRF token")

# Create a reusable dependency object for CSRF protection.
# This is used in the `dependencies` list of a router for state-changing endpoints.
CSRFProtect = Depends(csrf_protect)