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


def test_add_product_sale_and_list(client):
    create = client.post("/products", json={
        "name": "Gadget",
        "category": "Electronics",
        "price": 49.99,
        "stock": 25
    })
    assert create.status_code == 201

    products = client.get("/products").get_json()
    product_id = products[-1]["id"]

    sale = client.post(f"/products/{product_id}/sales", json={
        "quantity": 2,
        "sale_price": 45.00
    })
    assert sale.status_code == 201

    sales = client.get(f"/products/{product_id}/sales")
    assert sales.status_code == 200
    data = sales.get_json()
    assert isinstance(data, list)
    assert data[0]["product_id"] == product_id


def test_add_sale_missing_product(client):
    sale = client.post("/products/9999/sales", json={
        "quantity": 1,
        "sale_price": 9.99
    })
    assert sale.status_code == 404


def test_search(client):
    response = client.get("/search?q=widget")
    assert response.status_code == 200
