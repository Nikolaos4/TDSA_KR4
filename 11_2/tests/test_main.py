import pytest
from faker import Faker

fake = Faker()

@pytest.fixture
def random_user_data():
    return {
        "username": fake.user_name(),
        "age": fake.random_int(min=1, max=100)
    }

@pytest.mark.asyncio
async def test_create_user_success(client, random_user_data):
    response = await client.post("/users", json=random_user_data)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["username"] == random_user_data["username"]
    assert data["age"] == random_user_data["age"]

@pytest.mark.asyncio
async def test_create_user_invalid_data(client):
    response = await client.post("/users", json={"username": "onlyname"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_user_success(client, random_user_data):
    create_resp = await client.post("/users", json=random_user_data)
    user_id = create_resp.json()["id"]
    get_resp = await client.get(f"/users/{user_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == user_id
    assert data["username"] == random_user_data["username"]

@pytest.mark.asyncio
async def test_get_user_not_found(client):
    response = await client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_delete_user_success(client, random_user_data):
    create_resp = await client.post("/users", json=random_user_data)
    user_id = create_resp.json()["id"]
    del_resp = await client.delete(f"/users/{user_id}")
    assert del_resp.status_code == 204
    get_resp = await client.get(f"/users/{user_id}")
    assert get_resp.status_code == 404

@pytest.mark.asyncio
async def test_delete_user_not_found(client):
    response = await client.delete("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_delete_twice(client, random_user_data):
    create_resp = await client.post("/users", json=random_user_data)
    user_id = create_resp.json()["id"]
    del_resp1 = await client.delete(f"/users/{user_id}")
    assert del_resp1.status_code == 204
    del_resp2 = await client.delete(f"/users/{user_id}")
    assert del_resp2.status_code == 404