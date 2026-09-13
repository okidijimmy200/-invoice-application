from fastapi.testclient import TestClient

from tests.api.test_invoice_creation import customer_payload, invoice_payload


def test_reads_empty_and_populated_collections(client: TestClient) -> None:
    assert client.get("/api/v1/customers").json() == []
    assert client.get("/api/v1/invoices").json() == []
    assert client.get("/api/v1/customers/999").status_code == 404
    assert client.get("/api/v1/invoices/999").status_code == 404

    customer = client.post("/api/v1/customers", json=customer_payload()).json()
    invoice = client.post("/api/v1/invoices", json=invoice_payload(customer["id"])).json()
    assert client.get("/api/v1/customers").json()[0]["name"] == "Ada Lovelace"
    assert client.get("/api/v1/invoices").json()[0]["invoice_number"] == "INV-0001"
    detail = client.get(f"/api/v1/invoices/{invoice['id']}").json()
    assert detail["items"][0]["line_total"] == "39.98"
