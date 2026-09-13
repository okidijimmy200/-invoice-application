from fastapi.testclient import TestClient


def test_first_release_exposes_only_invoice_management_routes(client: TestClient) -> None:
    for path in ("/api/v1/auth", "/api/v1/payments", "/api/v1/emails", "/api/v1/recurring-invoices", "/api/v1/integrations"):
        assert client.get(path).status_code == 404
