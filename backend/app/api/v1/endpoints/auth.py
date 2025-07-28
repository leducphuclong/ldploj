from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# Import the necessary modules from your project structure
from backend.app import crud, schemas
from backend.app.api import deps

# Create a new router for authentication endpoints
router = APIRouter()


@router.post("/signup", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user_signup(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: schemas.UserCreate,
):
    """
    Create a new user account.

    This endpoint handles the user registration process.
    """
    # 1. Check if a user with this email already exists in the database.
    #    This uses the `get_by_email` method from your crud_user.py file.
    existing_user = await crud.user.get_by_email(db=db, email=user_in.email)
    if existing_user:
        # If the user exists, raise an HTTP 400 Bad Request error.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists.",
        )

    # 2. If the email is unique, proceed to create the new user.
    #    This calls the `create` method from your crud_user.py file.
    user = await crud.user.create(db=db, obj_in=user_in)

    # 3. Return the newly created user object.
    #    FastAPI will automatically filter the response based on the `schemas.User`
    #    response_model, so the hashed_password will not be sent to the client.
    return user