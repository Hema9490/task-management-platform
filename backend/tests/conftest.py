import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_project(client):
    resp = client.post("/api/projects", json={"name": "Website Revamp", "description": "Q3 redesign"})
    return resp.get_json()
