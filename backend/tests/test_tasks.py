def test_create_task(client, sample_project):
    resp = client.post("/api/tasks", json={
        "project_id": sample_project["id"],
        "title": "Design homepage",
        "priority": "high",
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["title"] == "Design homepage"
    assert data["status"] == "todo"
    assert data["priority"] == "high"


def test_create_task_requires_project_and_title(client):
    resp = client.post("/api/tasks", json={"title": "orphan task"})
    assert resp.status_code == 400


def test_create_task_rejects_unknown_project(client):
    resp = client.post("/api/tasks", json={"project_id": 999, "title": "ghost task"})
    assert resp.status_code == 404


def test_create_task_rejects_invalid_status(client, sample_project):
    resp = client.post("/api/tasks", json={
        "project_id": sample_project["id"], "title": "bad status", "status": "blocked"
    })
    assert resp.status_code == 400


def test_filter_tasks_by_project(client, sample_project):
    client.post("/api/tasks", json={"project_id": sample_project["id"], "title": "Task A"})
    resp = client.get(f"/api/tasks?project_id={sample_project['id']}")
    assert len(resp.get_json()) == 1


def test_filter_tasks_by_status(client, sample_project):
    client.post("/api/tasks", json={"project_id": sample_project["id"], "title": "Task A", "status": "done"})
    client.post("/api/tasks", json={"project_id": sample_project["id"], "title": "Task B", "status": "todo"})
    resp = client.get("/api/tasks?status=done")
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["title"] == "Task A"


def test_update_task_status_sets_closed_at(client, sample_project):
    created = client.post("/api/tasks", json={
        "project_id": sample_project["id"], "title": "Ship feature"
    }).get_json()
    resp = client.put(f"/api/tasks/{created['id']}", json={"status": "done"})
    data = resp.get_json()
    assert data["status"] == "done"
    assert data["closed_at"] is not None


def test_reopen_task_clears_closed_at(client, sample_project):
    created = client.post("/api/tasks", json={
        "project_id": sample_project["id"], "title": "Ship feature", "status": "done"
    }).get_json()
    resp = client.put(f"/api/tasks/{created['id']}", json={"status": "todo"})
    assert resp.get_json()["closed_at"] is None


def test_delete_task(client, sample_project):
    created = client.post("/api/tasks", json={
        "project_id": sample_project["id"], "title": "Temp task"
    }).get_json()
    resp = client.delete(f"/api/tasks/{created['id']}")
    assert resp.status_code == 200
    assert client.get(f"/api/tasks/{created['id']}").status_code == 404
