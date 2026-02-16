import pytest
from app import app, init_db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    init_db()
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get("/")
    data = response.get_json()
    assert response.status_code == 200
    assert data["app"] == "Acme Inventory API"


def test_list_products_empty(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_add_product(client):
    response = client.post("/products", json={
        "name": "Widget",
        "category": "Hardware",
        "price": 29.99,
        "stock": 100
    })
    assert response.status_code == 201


def test_search(client):
    response = client.get("/search?q=widget")
    assert response.status_code == 200
