import pytest


async def setup_project_with_auth(client, username="taskuser"):
    await client.post("/auth/register", json={
        "full_name": username,
        "username": username,
        "email": f"{username}@example.com",
        "password": "testpass123",
    })
    login_resp = await client.post("/auth/login", data={"username": username, "password": "testpass123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    project_resp = await client.post("/projects/", json={"name": "Task Test Project"}, headers=headers)
    project_id = project_resp.json()["id"]

    return headers, project_id


@pytest.mark.asyncio
async def test_create_task(client):
    headers, project_id = await setup_project_with_auth(client)
    response = await client.post(f"/projects/{project_id}/tasks/", json={
        "title": "Write tests",
        "description": "Cover core logic",
    }, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "todo"


@pytest.mark.asyncio
async def test_list_tasks_with_filter(client):
    headers, project_id = await setup_project_with_auth(client, username="filteruser")
    await client.post(f"/projects/{project_id}/tasks/", json={"title": "Task A"}, headers=headers)

    response = await client.get(f"/projects/{project_id}/tasks/?status=done", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


@pytest.mark.asyncio
async def test_update_task_status(client):
    headers, project_id = await setup_project_with_auth(client, username="updateuser")
    create_resp = await client.post(f"/projects/{project_id}/tasks/", json={"title": "Task B"}, headers=headers)
    task_id = create_resp.json()["id"]

    response = await client.put(f"/projects/{project_id}/tasks/{task_id}", json={"status": "done"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "done"


@pytest.mark.asyncio
async def test_delete_task(client):
    headers, project_id = await setup_project_with_auth(client, username="deleteuser")
    create_resp = await client.post(f"/projects/{project_id}/tasks/", json={"title": "Task C"}, headers=headers)
    task_id = create_resp.json()["id"]

    response = await client.delete(f"/projects/{project_id}/tasks/{task_id}", headers=headers)
    assert response.status_code == 403