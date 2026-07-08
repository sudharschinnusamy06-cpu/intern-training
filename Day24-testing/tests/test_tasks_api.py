def test_create_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Test task", "description": "Testing POST"},
        headers={"x-api-key": "myapikey123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test task"


def test_get_all_tasks(client):
    client.post(
        "/tasks",
        json={"title": "Task A", "description": "desc"},
        headers={"x-api-key": "myapikey123"},
    )

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_create_task_without_api_key(client):
    response = client.post(
        "/tasks",
        json={"title": "Sneaky task", "description": "No auth"},
    )

    assert response.status_code == 422


def test_create_task_with_wrong_api_key(client):
    response = client.post(
        "/tasks",
        json={"title": "Sneaky task", "description": "Wrong auth"},
        headers={"x-api-key": "totally-wrong-key"},
    )

    assert response.status_code == 401


def test_get_single_task(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Fetch me", "description": "single fetch test"},
        headers={"x-api-key": "myapikey123"},
    )
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Fetch me"


def test_get_single_task_not_found(client):
    response = client.get("/tasks/9999")

    assert response.status_code == 404


def test_update_task(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Old title", "description": "before update"},
        headers={"x-api-key": "myapikey123"},
    )
    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "New title", "description": "after update", "completed": True},
        headers={"x-api-key": "myapikey123"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "New title"
    assert response.json()["completed"]


def test_delete_task(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Delete me", "description": "will be removed"},
        headers={"x-api-key": "myapikey123"},
    )
    task_id = create_response.json()["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers={"x-api-key": "myapikey123"},
    )

    assert response.status_code == 200

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_update_task_not_found(client):
    response = client.put(
        "/tasks/9999",
        json={"title": "Doesn't matter", "description": "no task here", "completed": False},
        headers={"x-api-key": "myapikey123"},
    )

    assert response.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete(
        "/tasks/9999",
        headers={"x-api-key": "myapikey123"},
    )

    assert response.status_code == 404
