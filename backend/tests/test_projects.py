def test_health_check(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_create_project(client):
    resp = client.post("/api/projects", json={"name": "New App", "description": "MVP build"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == "New App"
    assert data["status"] == "active"
    assert data["task_count"] == 0


def test_create_project_requires_name(client):
    resp = client.post("/api/projects", json={"description": "no name here"})
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_list_projects(client, sample_project):
    resp = client.get("/api/projects")
    assert resp.status_code == 200
    projects = resp.get_json()
    assert len(projects) == 1
    assert projects[0]["name"] == "Website Revamp"


def test_get_single_project(client, sample_project):
    resp = client.get(f"/api/projects/{sample_project['id']}")
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "Website Revamp"


def test_get_missing_project_returns_404(client):
    resp = client.get("/api/projects/999")
    assert resp.status_code == 404


def test_update_project(client, sample_project):
    resp = client.put(f"/api/projects/{sample_project['id']}", json={"status": "archived"})
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "archived"


def test_delete_project(client, sample_project):
    resp = client.delete(f"/api/projects/{sample_project['id']}")
    assert resp.status_code == 200
    resp = client.get(f"/api/projects/{sample_project['id']}")
    assert resp.status_code == 404


def test_delete_project_cascades_tasks(client, sample_project):
    client.post("/api/tasks", json={"project_id": sample_project["id"], "title": "Design homepage"})
    client.delete(f"/api/projects/{sample_project['id']}")
    resp = client.get("/api/tasks")
    assert resp.get_json() == []
