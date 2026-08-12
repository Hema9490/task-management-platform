def _make_task(client, project_id, **overrides):
    payload = {"project_id": project_id, "title": "Task"}
    payload.update(overrides)
    return client.post("/api/tasks", json=payload).get_json()


def test_add_comment_to_task(client, sample_project):
    task = _make_task(client, sample_project["id"])
    resp = client.post(f"/api/tasks/{task['id']}/comments", json={
        "author": "Hema", "body": "Started working on this."
    })
    assert resp.status_code == 201
    assert resp.get_json()["body"] == "Started working on this."


def test_comment_requires_body(client, sample_project):
    task = _make_task(client, sample_project["id"])
    resp = client.post(f"/api/tasks/{task['id']}/comments", json={"author": "Hema"})
    assert resp.status_code == 400


def test_comment_on_missing_task_404(client):
    resp = client.post("/api/tasks/999/comments", json={"body": "hi"})
    assert resp.status_code == 404


def test_list_comments(client, sample_project):
    task = _make_task(client, sample_project["id"])
    client.post(f"/api/tasks/{task['id']}/comments", json={"body": "first"})
    client.post(f"/api/tasks/{task['id']}/comments", json={"body": "second"})
    resp = client.get(f"/api/tasks/{task['id']}/comments")
    assert len(resp.get_json()) == 2


def test_stats_overview(client, sample_project):
    _make_task(client, sample_project["id"], status="done")
    _make_task(client, sample_project["id"], status="todo")
    resp = client.get("/api/stats/overview")
    data = resp.get_json()
    assert data["total_tasks"] == 2
    assert data["done"] == 1
    assert data["todo"] == 1
    assert data["completion_rate_pct"] == 50.0


def test_stats_by_priority(client, sample_project):
    _make_task(client, sample_project["id"], priority="high")
    _make_task(client, sample_project["id"], priority="high")
    _make_task(client, sample_project["id"], priority="low")
    resp = client.get("/api/stats/by-priority")
    data = resp.get_json()
    assert data["high"] == 2
    assert data["low"] == 1


def test_stats_tasks_per_week(client, sample_project):
    _make_task(client, sample_project["id"])
    resp = client.get("/api/stats/tasks-per-week")
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["count"] == 1
