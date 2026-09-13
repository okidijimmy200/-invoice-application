from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.invoice import InvoiceInput, InvoiceListItem, InvoiceRead, InvoiceStatusChange
from app.services import invoices

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
def create_invoice(payload: InvoiceInput, db: Session = Depends(get_db)) -> InvoiceRead:
    return invoices.to_invoice_read(invoices.create_invoice(db, payload))


@router.get("", response_model=list[InvoiceListItem])
def list_invoices(db: Session = Depends(get_db)) -> list[InvoiceListItem]:
    return [invoices.to_invoice_list_item(invoice) for invoice in invoices.list_invoices(db)]


@router.get("/{invoice_id}", response_model=InvoiceRead)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)) -> InvoiceRead:
    return invoices.to_invoice_read(invoices._get_invoice(db, invoice_id))


@router.put("/{invoice_id}", response_model=InvoiceRead)
def update_invoice(invoice_id: int, payload: InvoiceInput, db: Session = Depends(get_db)) -> InvoiceRead:
    return invoices.to_invoice_read(invoices.update_invoice(db, invoice_id, payload))


@router.post("/{invoice_id}/status", response_model=InvoiceRead)
def change_status(
    invoice_id: int,
    payload: InvoiceStatusChange,
    db: Session = Depends(get_db),
) -> InvoiceRead:
    return invoices.to_invoice_read(invoices.change_status(db, invoice_id, payload.status))
