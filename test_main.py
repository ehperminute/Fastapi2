from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_lists():
    response = client.get("/lists")
    assert response.status_code == 200
    assert "task_lists" in response.json()


def test_create_list():
    response = client.post("/lists", json={"name": "Test List"})
    assert response.status_code in [200, 422]


def test_create_task_invalid_list():
    response = client.post("/tasks", json={"title": "Test Task", "list_id": 99999})
    assert response.status_code == 404

def test_create_duplicate_list():
    client.post("/lists", json={"name": "School"})
    response = client.post("/lists", json={"name": "School"})
    assert response.status_code == 422
