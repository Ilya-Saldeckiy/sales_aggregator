import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_add_sales():
    payload = [
        {
            "order_id": "TEST-1",
            "marketplace": "ozon",
            "product_name": "Product 1",
            "quantity": 2,
            "price": 1000.0,
            "cost_price": 500.0,
            "status": "delivered",
            "sold_at": "2026-04-10"
        }
    ]
    response = client.post("/sales", json=payload)
    assert response.status_code == 200
    assert response.json()["added_count"] == 1

def test_get_analytics_summary():
    test_add_sales()
    response = client.get("/analytics/summary?date_from=2026-01-01&date_to=2026-12-31")
    assert response.status_code == 200
    data = response.json()[0]
    assert data["total_revenue"] == 2000.0
    assert data["gross_profit"] == 1000.0

def test_invalid_date_future():
    payload = [{
        "order_id": "ERR-1", "marketplace": "ozon", "product_name": "X",
        "quantity": 1, "price": 10, "cost_price": 5, "status": "delivered",
        "sold_at": "2099-01-01"
    }]
    response = client.post("/sales", json=payload)
    assert response.status_code == 422