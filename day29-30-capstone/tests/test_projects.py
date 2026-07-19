import pytest


async def get_auth_headers(client, username="projectuser", password="testpass123"):
    await client.post("/auth/register", json={
        "full_name": username,
        "username": username,
        "email": f"{username}@example.com",
        "password": password,
    })
    response = await client.post("/auth/login", data={"username": username, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_project(client):
    headers = await get_auth_headers(client)
    response = await client.post("/projects/", json={
        "name": "Test Project",
        "description": "A test project",
    }, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"


@pytest.mark.asyncio
async def test_list_projects(client):
    headers = await get_auth_headers(client, username="listuser")
    await client.post("/projects/", json={"name": "P1"}, headers=headers)
    response = await client.get("/projects/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


@pytest.mark.asyncio
async def test_get_nonexistent_project(client):
    headers = await get_auth_headers(client, username="notfounduser")
    response = await client.get("/projects/999", headers=headers)
    assert response.status_code == 404