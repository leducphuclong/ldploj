from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from ..db.base import Base
import typing

if typing.TYPE_CHECKING:
    from .post import Post 

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    posts: Mapped[List["Post"]] = relationship(back_populates="owner")