import pytest
import sys
import os
from fastapi.testclient import TestClient
# Ensure the app module is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.main import app

client = TestClient(app)

def test_create_new_product():
    # Example payload, adjust fields as needed
    payload = {
        "title": "Test Product",
        "description": "A product for testing.",
        "price": 10.0,
        "category_id": 1,
        "condition": "new",
        "location": "Test City"
    }
    response = client.post("/products/", json=payload)
    assert response.status_code == 200 or response.status_code == 201
    assert "id" in response.json()

def test_patch_product_by_id():
    # First, create a product
    payload = {
        "title": "Patch Product",
        "description": "Patch test.",
        "price": 20.0,
        "category_id": 1,
        "condition": "used",
        "location": "Patch City"
    }
    create_resp = client.post("/products/", json=payload)
    product_id = create_resp.json()["id"]
    # Patch the product
    patch_payload = {"price": 25.0}
    patch_resp = client.patch(f"/products/{product_id}", json=patch_payload)
    assert patch_resp.status_code == 200
    assert patch_resp.json()["price"] == 25.0

def test_create_products_batch():
    batch_payload = [
        {
            "title": "Batch Product 1",
            "description": "Batch 1.",
            "price": 5.0,
            "category_id": 1,
            "condition": "new",
            "location": "Batch City"
        },
        {
            "title": "Batch Product 2",
            "description": "Batch 2.",
            "price": 15.0,
            "category_id": 1,
            "condition": "used",
            "location": "Batch City"
        }
    ]
    response = client.post("/products/batch", json=batch_payload)
    assert response.status_code == 200 or response.status_code == 201
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2

def test_read_products_with_filter():
    response = client.get("/products/?min_price=5&max_price=20")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
