def test_create_task(client):
    response = client.post(
        "/v1/tasks",
        json={"title": "Test task", "description": "Testing POST"},
        headers={"x-api-key": "myapikey123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test task"


def test_get_all_tasks(client):
    client.post(
        "/v1/tasks",
        json={"title": "Task A", "description": "desc"},
        headers={"x-api-key": "myapikey123"},
    )

    response = client.get("/v1/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_create_task_without_api_key(client):
    response = client.post(
        "/v1/tasks",
        json={"title": "Sneaky task", "description": "No auth"},
    )

    assert response.status_code == 422


def test_create_task_with_wrong_api_key(client):
    response = client.post(
        "/v1/tasks",
        json={"title": "Sneaky task", "description": "Wrong auth"},
        headers={"x-api-key": "totally-wrong-key"},
    )

    assert response.status_code == 401


def test_get_single_task(client):
    create_response = client.post(
        "/v1/tasks",
        json={"title": "Fetch me", "description": "single fetch test"},
        headers={"x-api-key": "myapikey123"},
    )
    task_id = create_response.json()["id"]

    response = client.get(f"/v1/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Fetch me"


def test_get_single_task_not_found(client):
    response = client.get("/v1/tasks/9999")

    assert response.status_code == 404


def test_update_task(client):
    create_response = client.post(
        "/v1/tasks",
        json={"title": "Old title", "description": "before update"},
        headers={"x-api-key": "myapikey123"},
    )
    task_id = create_response.json()["id"]

    response = client.put(
        f"/v1/tasks/{task_id}",
        json={"title": "New title", "description": "after update", "completed": True},
        headers={"x-api-key": "myapikey123"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "New title"
    assert response.json()["completed"]


def test_delete_task(client):
    create_response = client.post(
        "/v1/tasks",
        json={"title": "Delete me", "description": "will be removed"},
        headers={"x-api-key": "myapikey123"},
    )
    task_id = create_response.json()["id"]

    response = client.delete(
        f"/v1/tasks/{task_id}",
        headers={"x-api-key": "myapikey123"},
    )

    assert response.status_code == 200

    get_response = client.get(f"/v1/tasks/{task_id}")
    assert get_response.status_code == 404


def test_update_task_not_found(client):
    response = client.put(
        "/v1/tasks/9999",
        json={"title": "Doesn't matter", "description": "no task here", "completed": False},
        headers={"x-api-key": "myapikey123"},
    )

    assert response.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete(
        "/v1/tasks/9999",
        headers={"x-api-key": "myapikey123"},
    )

    assert response.status_code == 404


def test_pagination_limit(client):
    client.post(
        "/v1/tasks",
        json={"title": "Task 1", "description": "d1"},
        headers={"x-api-key": "myapikey123"},
    )
    client.post(
        "/v1/tasks",
        json={"title": "Task 2", "description": "d2"},
        headers={"x-api-key": "myapikey123"},
    )
    client.post(
        "/v1/tasks",
        json={"title": "Task 3", "description": "d3"},
        headers={"x-api-key": "myapikey123"},
    )

    response = client.get("/v1/tasks?limit=2")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_filter_completed(client):
    client.post(
        "/v1/tasks",
        json={"title": "Done task", "description": "d1", "completed": True},
        headers={"x-api-key": "myapikey123"},
    )
    client.post(
        "/v1/tasks",
        json={"title": "Not done task", "description": "d2", "completed": False},
        headers={"x-api-key": "myapikey123"},
    )

    response = client.get("/v1/tasks?completed=true")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Done task"

def test_pagination_negative_skip(client):
    response = client.get("/v1/tasks?skip=-5")

    assert response.status_code == 200
    assert response.json() == []


def test_pagination_invalid_limit_type(client):
    response = client.get("/v1/tasks?limit=abc")

    assert response.status_code == 422