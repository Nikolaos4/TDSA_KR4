import pytest
from app.main import fake_db

def reset_db():
    fake_db.clear()
    import app.main
    app.main.current_id = 1

@pytest.fixture(autouse=True)
def clean_db():
    """Автоматически очищает хранилище перед каждым тестом."""
    reset_db()
    yield


def test_create_user_success(client):
    response = client.post("/users/", json={
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30
    })
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["age"] == 30

def test_create_user_invalid_data(client):
    response = client.post("/users/", json={
        "name": "Bob",
        "age": 25
    })
    assert response.status_code == 422
    assert "detail" in response.json()

@pytest.mark.parametrize("payload, expected_status", [
    ({"email": "bob@test.com", "age": 20}, 422),   # нет name
    ({"name": "Bob", "age": 20}, 422),             # нет email
])
def test_create_user_validation_errors(client, payload, expected_status):
    response = client.post("/users/", json=payload)
    assert response.status_code == expected_status


def test_get_user_success(client):
    client.post("/users/", json={"name": "Charlie", "email": "charlie@test.com", "age": 28})
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Charlie"

def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_user_success(client):
    client.post("/users/", json={"name": "Diana", "email": "diana@test.com", "age": 35})
    delete_resp = client.delete("/users/1")
    assert delete_resp.status_code == 204
    get_resp = client.get("/users/1")
    assert get_resp.status_code == 404

def test_delete_user_not_found(client):
    response = client.delete("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_list_users(client):
    client.post("/users/", json={"name": "Eve", "email": "eve@test.com", "age": 22})
    client.post("/users/", json={"name": "Frank", "email": "frank@test.com", "age": 45})
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Eve"
    assert data[1]["name"] == "Frank"