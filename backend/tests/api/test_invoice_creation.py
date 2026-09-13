from fastapi.testclient import TestClient


def customer_payload() -> dict[str, str]:
    return {"name": "Ada Lovelace", "phone": "+1 555 0100", "email": "ada@example.com", "address": "1 Main St"}


def invoice_payload(customer_id: int) -> dict[str, object]:
    return {
        "customer_id": customer_id,
        "issue_date": "2026-01-01",
        "due_date": "2026-01-31",
        "notes": "Thank you",
        "payment_terms": "Net 30",
        "items": [
            {"description": "Design", "quantity": "2", "unit_price": "19.99"},
            {"description": "Support", "quantity": "1", "unit_price": "10.00"},
        ],
    }


def test_creates_customer_and_invoice_with_server_totals(client: TestClient) -> None:
    customer = client.post("/api/v1/customers", json=customer_payload())
    assert customer.status_code == 201

    response = client.post("/api/v1/invoices", json=invoice_payload(customer.json()["id"]))
    assert response.status_code == 201
    body = response.json()
    assert body["invoice_number"] == "INV-0001"
    assert body["status"] == "Draft"
    assert body["subtotal"] == "49.98"
    assert body["tax"] == "7.50"
    assert body["total"] == "57.48"


def test_rejects_invalid_boundary_data(client: TestClient) -> None:
    assert client.post("/api/v1/customers", json={**customer_payload(), "email": "bad"}).status_code == 422
    customer = client.post("/api/v1/customers", json=customer_payload()).json()

    bad_date = invoice_payload(customer["id"])
    bad_date["due_date"] = "2025-12-31"
    assert client.post("/api/v1/invoices", json=bad_date).status_code == 422

    bad_item = invoice_payload(customer["id"])
    bad_item["items"] = [{"description": "", "quantity": "0", "unit_price": "-1"}]
    assert client.post("/api/v1/invoices", json=bad_item).status_code == 422
