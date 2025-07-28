from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional

# We need to import the Post schema to define the relationship.
# This creates a circular import, but Pydantic handles it because we use
# model_rebuild() at the end of the file.
from .post import Post


# --- Base Schema ---
# Contains shared properties that other schemas will inherit.
class UserBase(BaseModel):
    email: EmailStr


# --- Creation Schema ---
# Defines the shape of data the API expects when creating a new user.
# It inherits from UserBase and adds the password.
class UserCreate(UserBase):
    password: str


# --- Response Schema ---
# This is the "public" view of the user model.
# It defines the data that is sent back to the client.
# CRUCIALLY, it does NOT include the password.
class User(UserBase):
    id: int
    posts: List[Post] = []  # This will be populated from the ORM relationship

    # Pydantic V2 config to enable creating this schema from a SQLAlchemy model instance.
    # It tells Pydantic to read data from object attributes (e.g., user.id)
    # instead of just dictionary keys (e.g., user['id']).
    model_config = ConfigDict(from_attributes=True)


# --- Internal Schema for Security ---
# Used for validating the data (payload) inside a JWT token.
class TokenData(BaseModel):
    email: Optional[str] = None


# --- Resolve Circular Dependencies ---
# This is a crucial step in Pydantic V2.
# The `User` schema depends on the `Post` schema, and the `Post` schema depends on `User`.
# After both models are fully defined in their respective files, `model_rebuild()`
# tells Pydantic to go back and correctly wire up these cross-references.
User.model_rebuild()