from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..core.security import get_password_hash
from ..models import user as user_model, post as post_model
from ..schemas import user as user_schema, post as post_schema

async def get_user_by_email(db: AsyncSession, email: str) -> user_model.User | None:
    result = await db.execute(select(user_model.User).filter(user_model.User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: user_schema.UserCreate) -> user_model.User:
    hashed_password = get_password_hash(user.password)
    db_user = user_model.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def create_post(db: AsyncSession, post: post_schema.PostCreate, owner_id: int) -> post_model.Post:
    db_post = post_model.Post(**post.dict(), owner_id=owner_id)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(post_model.Post).offset(skip).limit(limit))
    return result.scalars().all()