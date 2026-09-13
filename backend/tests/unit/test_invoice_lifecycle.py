from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from app.api.errors import ConflictError
from app.models.invoice import InvoiceStatus
from app.schemas.customer import CustomerCreate
from app.schemas.invoice import InvoiceInput, InvoiceItemInput
from app.services.customers import create_customer
from app.services.invoices import change_status, create_invoice, update_invoice


def payload(customer_id: int, price: str = "10.00") -> InvoiceInput:
    return InvoiceInput(
        customer_id=customer_id,
        issue_date=date(2026, 1, 1),
        due_date=date(2026, 1, 31),
        items=[InvoiceItemInput(description="Work", quantity=Decimal("1"), unit_price=Decimal(price))],
    )


def test_status_graph_and_draft_only_editing(db: Session) -> None:
    customer = create_customer(db, CustomerCreate(name="Ada", phone="1", email="ada@example.com", address="A"))
    invoice = create_invoice(db, payload(customer.id))
    edited = update_invoice(db, invoice.id, payload(customer.id, "20.00"))
    assert edited.total_cents == 2300

    sent = change_status(db, invoice.id, InvoiceStatus.SENT)
    assert sent.status == InvoiceStatus.SENT
    with pytest.raises(ConflictError):
        update_invoice(db, invoice.id, payload(customer.id))
    with pytest.raises(ConflictError):
        change_status(db, invoice.id, InvoiceStatus.DRAFT)

    paid = change_status(db, invoice.id, InvoiceStatus.PAID)
    with pytest.raises(ConflictError):
        change_status(db, paid.id, InvoiceStatus.CANCELLED)
