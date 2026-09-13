from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.errors import NotFoundError
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate


def create_customer(db: Session, payload: CustomerCreate) -> Customer:
    customer = Customer(**payload.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def list_customers(db: Session) -> list[Customer]:
    return list(db.scalars(select(Customer).order_by(Customer.name, Customer.id)))


def get_customer(db: Session, customer_id: int) -> Customer:
    customer = db.get(Customer, customer_id)
    if customer is None:
        raise NotFoundError("Customer not found")
    return customer
