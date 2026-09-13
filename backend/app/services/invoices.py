from __future__ import annotations

from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.api.errors import ConflictError, NotFoundError
from app.models.customer import Customer
from app.models.invoice import Invoice, InvoiceItem, InvoiceStatus
from app.schemas.invoice import (
    CustomerSummary,
    InvoiceInput,
    InvoiceItemRead,
    InvoiceListItem,
    InvoiceRead,
)
from app.services.calculations import calculate_invoice, format_money, format_quantity

ALLOWED_TRANSITIONS: dict[InvoiceStatus, set[InvoiceStatus]] = {
    InvoiceStatus.DRAFT: {InvoiceStatus.SENT, InvoiceStatus.CANCELLED},
    InvoiceStatus.SENT: {InvoiceStatus.PAID, InvoiceStatus.OVERDUE, InvoiceStatus.CANCELLED},
    InvoiceStatus.OVERDUE: {InvoiceStatus.CANCELLED},
    InvoiceStatus.PAID: set(),
    InvoiceStatus.CANCELLED: set(),
}


def _get_invoice(db: Session, invoice_id: int) -> Invoice:
    statement = (
        select(Invoice)
        .where(Invoice.id == invoice_id)
        .options(selectinload(Invoice.customer), selectinload(Invoice.items))
    )
    invoice = db.scalar(statement)
    if invoice is None:
        raise NotFoundError("Invoice not found")
    return invoice


def _require_customer(db: Session, customer_id: int) -> Customer:
    customer = db.get(Customer, customer_id)
    if customer is None:
        raise NotFoundError("Customer not found")
    return customer


def _apply_input(invoice: Invoice, payload: InvoiceInput) -> None:
    totals = calculate_invoice([(item.quantity, item.unit_price) for item in payload.items])
    invoice.customer_id = payload.customer_id
    invoice.issue_date = payload.issue_date
    invoice.due_date = payload.due_date
    invoice.notes = payload.notes
    invoice.payment_terms = payload.payment_terms
    invoice.subtotal_cents = totals.subtotal_cents
    invoice.tax_cents = totals.tax_cents
    invoice.total_cents = totals.total_cents
    invoice.items.clear()
    for request_item, calculated in zip(payload.items, totals.items, strict=True):
        invoice.items.append(
            InvoiceItem(
                description=request_item.description,
                quantity_millis=calculated.quantity_millis,
                unit_price_cents=calculated.unit_price_cents,
                line_total_cents=calculated.line_total_cents,
            )
        )


def create_invoice(db: Session, payload: InvoiceInput) -> Invoice:
    _require_customer(db, payload.customer_id)
    invoice = Invoice(
        invoice_number=f"PENDING-{uuid4().hex}",
        customer_id=payload.customer_id,
        issue_date=payload.issue_date,
        due_date=payload.due_date,
        status=InvoiceStatus.DRAFT,
        subtotal_cents=0,
        tax_cents=0,
        total_cents=0,
        notes="",
        payment_terms="",
    )
    _apply_input(invoice, payload)
    try:
        db.add(invoice)
        db.flush()
        invoice.invoice_number = f"INV-{invoice.id:04d}"
        db.commit()
    except Exception:
        db.rollback()
        raise
    return _get_invoice(db, invoice.id)


def update_invoice(db: Session, invoice_id: int, payload: InvoiceInput) -> Invoice:
    invoice = _get_invoice(db, invoice_id)
    if invoice.status != InvoiceStatus.DRAFT:
        raise ConflictError("Only Draft invoices can be edited")
    _require_customer(db, payload.customer_id)
    _apply_input(invoice, payload)
    db.commit()
    return _get_invoice(db, invoice_id)


def change_status(db: Session, invoice_id: int, new_status: InvoiceStatus) -> Invoice:
    invoice = _get_invoice(db, invoice_id)
    if new_status not in ALLOWED_TRANSITIONS[invoice.status]:
        raise ConflictError(f"Cannot change {invoice.status.value} invoice to {new_status.value}")
    invoice.status = new_status
    db.commit()
    return _get_invoice(db, invoice_id)


def list_invoices(db: Session) -> list[Invoice]:
    statement = select(Invoice).options(selectinload(Invoice.customer)).order_by(Invoice.id.desc())
    return list(db.scalars(statement))


def to_invoice_list_item(invoice: Invoice) -> InvoiceListItem:
    return InvoiceListItem(
        id=invoice.id,
        invoice_number=invoice.invoice_number,
        customer_id=invoice.customer_id,
        customer_name=invoice.customer.name,
        issue_date=invoice.issue_date,
        due_date=invoice.due_date,
        status=invoice.status,
        total=format_money(invoice.total_cents),
    )


def to_invoice_read(invoice: Invoice) -> InvoiceRead:
    return InvoiceRead(
        **to_invoice_list_item(invoice).model_dump(),
        customer=CustomerSummary(
            id=invoice.customer.id,
            name=invoice.customer.name,
            phone=invoice.customer.phone,
            email=invoice.customer.email,
            address=invoice.customer.address,
        ),
        items=[
            InvoiceItemRead(
                id=item.id,
                description=item.description,
                quantity=format_quantity(item.quantity_millis),
                unit_price=format_money(item.unit_price_cents),
                line_total=format_money(item.line_total_cents),
            )
            for item in invoice.items
        ],
        subtotal=format_money(invoice.subtotal_cents),
        tax=format_money(invoice.tax_cents),
        notes=invoice.notes,
        payment_terms=invoice.payment_terms,
    )
