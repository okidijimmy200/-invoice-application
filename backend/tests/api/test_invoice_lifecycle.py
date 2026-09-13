from fastapi.testclient import TestClient

from tests.api.test_invoice_creation import customer_payload, invoice_payload


def test_edits_draft_and_enforces_status_lifecycle(client: TestClient) -> None:
    customer = client.post("/api/v1/customers", json=customer_payload()).json()
    invoice = client.post("/api/v1/invoices", json=invoice_payload(customer["id"])).json()
    edited = invoice_payload(customer["id"])
    edited["items"] = [{"description": "Updated", "quantity": "1", "unit_price": "20.00"}]
    assert client.put(f"/api/v1/invoices/{invoice['id']}", json=edited).json()["total"] == "23.00"
    assert client.post(f"/api/v1/invoices/{invoice['id']}/status", json={"status": "Sent"}).status_code == 200
    assert client.put(f"/api/v1/invoices/{invoice['id']}", json=edited).status_code == 409
    assert client.post(f"/api/v1/invoices/{invoice['id']}/status", json={"status": "Draft"}).status_code == 409
    assert client.post(f"/api/v1/invoices/{invoice['id']}/status", json={"status": "Paid"}).json()["status"] == "Paid"
