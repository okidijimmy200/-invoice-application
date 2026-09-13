from fastapi import APIRouter

from app.api.routes.customers import router as customers_router
from app.api.routes.invoices import router as invoices_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(customers_router)
api_router.include_router(invoices_router)
