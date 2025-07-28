from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ....schemas.post import Post, PostCreate
from ....db import crud
from ....db.session import get_db

router = APIRouter()

@router.post("/", response_model=Post, status_code=201)
def create_new_post(post: PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post)

@router.get("/", response_model=List[Post])
def read_all_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts