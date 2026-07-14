import pytest


@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post("/auth/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass123",
    })
    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "testuser"
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_username(client):
    await client.post("/auth/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass123",
    })
    response = await client.post("/auth/register", json={
        "username": "testuser",
        "email": "different@example.com",
        "password": "testpass123",
    })
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/auth/register", json={
        "username": "loginuser",
        "email": "loginuser@example.com",
        "password": "testpass123",
    })
    response = await client.post("/auth/login", data={
        "username": "loginuser",
        "password": "testpass123",
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post("/auth/register", json={
        "username": "wronguser",
        "email": "wronguser@example.com",
        "password": "testpass123",
    })
    response = await client.post("/auth/login", data={
        "username": "wronguser",
        "password": "wrongpassword",
    })
    assert response.status_code == 401