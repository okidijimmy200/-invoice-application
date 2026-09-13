from datetime import date
from decimal import Decimal

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.models.invoice import Invoice
from app.schemas.customer import CustomerCreate
from app.schemas.invoice import InvoiceInput, InvoiceItemInput
from app.services.customers import create_customer
from app.services.invoices import create_invoice


def invoice_payload(customer_id: int) -> InvoiceInput:
    return InvoiceInput(
        customer_id=customer_id,
        issue_date=date(2026, 1, 1),
        due_date=date(2026, 1, 31),
        items=[InvoiceItemInput(description="Work", quantity=Decimal("1"), unit_price=Decimal("10.00"))],
    )


def test_numbers_are_sequential_and_not_reused(db: Session) -> None:
    customer = create_customer(db, CustomerCreate(name="Ada", phone="1", email="ada@example.com", address="A"))
    first = create_invoice(db, invoice_payload(customer.id))
    db.execute(delete(Invoice).where(Invoice.id == first.id))
    db.commit()
    second = create_invoice(db, invoice_payload(customer.id))

    assert first.invoice_number == "INV-0001"
    assert second.invoice_number == "INV-0002"
