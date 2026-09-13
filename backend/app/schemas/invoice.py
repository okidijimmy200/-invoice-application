from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.invoice import InvoiceStatus


def _validate_decimal(value: object, *, label: str, positive: bool, places: int) -> Decimal:
    if isinstance(value, float):
        raise ValueError(f"{label} must be sent as a decimal string, not a float")
    try:
        decimal_value = Decimal(str(value))
    except Exception as exc:
        raise ValueError(f"{label} must be a decimal value") from exc
    if not decimal_value.is_finite():
        raise ValueError(f"{label} must be finite")
    if (positive and decimal_value <= 0) or (not positive and decimal_value < 0):
        comparison = "greater than zero" if positive else "zero or greater"
        raise ValueError(f"{label} must be {comparison}")
    if -decimal_value.as_tuple().exponent > places:
        raise ValueError(f"{label} supports at most {places} decimal places")
    return decimal_value


class InvoiceItemInput(BaseModel):
    description: str
    quantity: Decimal
    unit_price: Decimal

    @field_validator("description")
    @classmethod
    def non_blank_description(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Description must not be blank")
        return value

    @field_validator("quantity", mode="before")
    @classmethod
    def valid_quantity(cls, value: object) -> Decimal:
        return _validate_decimal(value, label="Quantity", positive=True, places=3)

    @field_validator("unit_price", mode="before")
    @classmethod
    def valid_unit_price(cls, value: object) -> Decimal:
        return _validate_decimal(value, label="Unit price", positive=False, places=2)


class InvoiceInput(BaseModel):
    customer_id: int = Field(gt=0)
    issue_date: date
    due_date: date
    items: list[InvoiceItemInput] = Field(min_length=1)
    notes: str = ""
    payment_terms: str = ""

    @model_validator(mode="after")
    def due_date_not_before_issue_date(self) -> "InvoiceInput":
        if self.due_date < self.issue_date:
            raise ValueError("Due date must not be earlier than issue date")
        return self


class InvoiceStatusChange(BaseModel):
    status: InvoiceStatus


class InvoiceItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str
    quantity: str
    unit_price: str
    line_total: str


class InvoiceListItem(BaseModel):
    id: int
    invoice_number: str
    customer_id: int
    customer_name: str
    issue_date: date
    due_date: date
    status: InvoiceStatus
    total: str


class InvoiceRead(InvoiceListItem):
    customer: "CustomerSummary"
    items: list[InvoiceItemRead]
    subtotal: str
    tax: str
    notes: str
    payment_terms: str


class CustomerSummary(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    address: str


InvoiceRead.model_rebuild()
