# Quickstart: Invoice Management Validation

## Prerequisites

- Python 3.11 or later
- Node.js LTS and npm

## Local Setup

1. Create and activate the backend virtual environment:

   ```sh
   cd backend
   python3.11 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Start the backend in one terminal:

   ```sh
   cd backend
   source .venv/bin/activate
   uvicorn app.main:app --reload
   ```

3. Install and start the frontend in another terminal:

   ```sh
   cd frontend
   npm install
   npm run dev
   ```

4. Open the Vite local URL. Its development proxy sends `/api/v1` calls to the backend.

## Automated Validation

```sh
cd backend
source .venv/bin/activate
pytest

cd ../frontend
npm run build
```

The backend suite must cover calculation, tax, validation, numbering, lifecycle, and Draft-edit scenarios
from [plan.md](plan.md). The frontend build must complete without type errors.

## End-to-End Validation

1. Create a customer with all four required contact fields and confirm it appears in the customer list.
2. Create a Draft with valid dates, notes, payment terms, and two items. Confirm the first number is
   `INV-0001` and all server-returned money uses fixed two-place USD strings.
3. Confirm each line total, subtotal, 15% tax, and total match the rules in
   [data-model.md](data-model.md).
4. Edit the Draft and confirm totals recalculate. Send it, verify further editing is refused, then test
   Sent → Paid and a separate Sent → Overdue → Cancelled path.
5. Attempt a blank customer field, invalid email, due date before issue date, empty item list, zero
   quantity, negative price, and invalid transition. Confirm each is rejected without changing saved data.
6. Open an invoice detail, choose Print, and verify the preview shows number, dates, customer, status,
   items, totals, notes, and payment terms.

See [contracts/openapi.yaml](contracts/openapi.yaml) for request and response shapes.

## Validation Record — 2026-09-09

- Backend automated suite: PASS (10 tests). It verifies customer/invoice creation, exact line/subtotal/tax/
  total calculations, 15% tax, validation failures, generated numbers, no-reuse behavior, reads, Draft-only
  editing, status conflicts, and excluded API routes.
- Frontend production build: PASS (`npm run build`).
- Print readiness: the invoice detail includes every required field and its dedicated print stylesheet hides
  application controls while preserving the customer, items, totals, notes, and payment terms.
