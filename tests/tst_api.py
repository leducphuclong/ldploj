# tests/test_api.py

import pytest
from httpx import AsyncClient

# Mark all tests in this file as async
pytestmark = pytest.mark.asyncio

# --- Test User Auth Flow ---

async def test_signup(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/signup",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data

async def test_login_and_get_cookies(client: AsyncClient):
    await client.post(
        "/api/v1/auth/signup",
        json={"email": "login@example.com", "password": "password123"},
    )
    login_data = {"username": "login@example.com", "password": "password123"}
    response = await client.post("/api/v1/auth/login", data=login_data)
    
    assert response.status_code == 200
    assert "access_token" in response.cookies
    assert "csrf_token" in response.cookies
    assert response.cookies.get_dict()["access_token"]["httponly"] is True

# ... (all other tests from the previous guide's test_api.py are still valid) ...

async def test_create_post_protected(client: AsyncClient):
    await client.post("/api/v1/auth/signup", json={"email": "poster@example.com", "password": "password123"})
    await client.post("/api/v1/auth/login", data={"username": "poster@example.com", "password": "password123"})
    
    csrf_token = client.cookies.get("csrf_token")
    assert csrf_token is not None
    
    post_data = {"title": "My Test Post", "content": "This is a test."}
    headers = {"x-csrf-token": csrf_token}
    
    response = await client.post("/api/v1/posts/", json=post_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "My Test Post"