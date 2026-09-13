---

description: "Dependency-ordered implementation tasks for Invoice Management"
---

# Tasks: Invoice Management

**Input**: Design documents from `/specs/001-invoice-management/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md),
[data-model.md](data-model.md), [contracts/openapi.yaml](contracts/openapi.yaml), and
[quickstart.md](quickstart.md)

**Tests**: Required. The specification and constitution require automated coverage for invoice calculations,
15% tax, validation, invoice numbering, status transitions, Draft-only editing, and API edge cases.

**Organization**: Tasks are grouped by user story so each increment can be implemented and validated
separately after the shared foundation is complete.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel with other marked tasks after its stated dependency is met
- **[Story]**: The user story the task implements
- Every task includes its exact target path

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the small monorepo, its dependency manifests, and development configuration.

- [X] T001 Create the backend/frontend directory tree and ignore virtual environments, SQLite files, build output, and local environment files in `.gitignore`
- [X] T002 Create the Python 3.11 backend dependency manifest in `backend/requirements.txt` with FastAPI, SQLAlchemy, Pydantic, Uvicorn, pytest, and HTTP test support only
- [X] T003 [P] Initialize the React/TypeScript/Vite application and dependency manifest in `frontend/package.json`
- [X] T004 [P] Configure the Vite `/api/v1` development proxy in `frontend/vite.config.ts`
- [X] T005 [P] Add the frontend application entry point and route shell in `frontend/src/main.tsx` and `frontend/src/App.tsx`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish database, FastAPI, shared errors, and isolated test infrastructure. No user-story
implementation begins before this phase is complete.

- [X] T006 Configure the SQLite engine, session factory, and request-scoped database dependency in `backend/app/db/session.py`
- [X] T007 Create SQLAlchemy declarative metadata and model imports in `backend/app/db/base.py` and `backend/app/models/__init__.py`
- [X] T008 [P] Create stable domain error types and FastAPI error mapping for 404 and 409 responses in `backend/app/api/errors.py`
- [X] T009 Create the FastAPI application, explicit development CORS setup, health route, and API router registration in `backend/app/main.py`
- [X] T010 Create temporary SQLite database/session and FastAPI client fixtures in `backend/tests/conftest.py`
- [X] T011 Create the API router package and `/api/v1` route composition in `backend/app/api/router.py` and `backend/app/api/routes/__init__.py`

**Checkpoint**: Database sessions, test isolation, application boot, and error conventions are ready.

---

## Phase 3: User Story 1 - Create a Customer and Draft Invoice (Priority: P1) 🎯 MVP

**Goal**: A user creates a fully valid customer and a Draft invoice with server-derived, exact USD totals
and an immutable generated invoice number.

**Independent Test**: Create a customer and a two-item Draft through the API/UI; verify `INV-0001`, all
saved fields, and line/subtotal/tax/total values without relying on a later story.

### Tests for User Story 1

- [X] T012 [P] [US1] Write calculation and rounding unit tests, including 15% tax, zero price, fractional quantities, and changed Decimal context in `backend/tests/unit/test_calculations.py`
- [X] T013 [P] [US1] Write invoice-service tests for generated `INV-0001` numbering, no reuse after deletion, and unique persistence in `backend/tests/unit/test_invoice_service.py`
- [X] T014 [P] [US1] Write API tests for valid customer/invoice creation and invalid customer, date, item, quantity, and price input in `backend/tests/api/test_invoice_creation.py`

### Implementation for User Story 1

- [X] T015 [P] [US1] Define the Customer SQLAlchemy table and its invoice relationship in `backend/app/models/customer.py`
- [X] T016 [US1] Define Invoice and InvoiceItem tables with AUTOINCREMENT ID, unique immutable invoice number, integer-cent totals, scaled quantities, and relationships in `backend/app/models/invoice.py` and `backend/app/models/invoice_item.py`
- [X] T017 [P] [US1] Define Pydantic customer create/read schemas with trimmed required fields and email validation in `backend/app/schemas/customer.py`
- [X] T018 [US1] Define Pydantic invoice and item input/read schemas that accept decimal strings, reject invalid dates/items, and return derived money as two-place strings in `backend/app/schemas/invoice.py`
- [X] T019 [US1] Implement pure Decimal-to-cent calculation, explicit `ROUND_HALF_UP`, fixed 15% tax, and output formatting in `backend/app/services/calculations.py`
- [X] T020 [US1] Implement customer creation and retrieval service methods in `backend/app/services/customers.py`
- [X] T021 [US1] Implement atomic Draft creation, server-only total derivation, customer existence checks, and post-flush `INV-{id:04d}` assignment in `backend/app/services/invoices.py`
- [X] T022 [US1] Implement `POST /customers` in `backend/app/api/routes/customers.py` using schemas and customer service methods
- [X] T023 [US1] Implement `POST /invoices` in `backend/app/api/routes/invoices.py` using invoice schemas, service errors, and the Draft response contract
- [X] T024 [P] [US1] Define shared customer/invoice/line-item request-response types with decimal-string money fields in `frontend/src/types/customer.ts` and `frontend/src/types/invoice.ts`
- [X] T025 [P] [US1] Implement fetch/error normalization and create operations in `frontend/src/api/client.ts`, `frontend/src/api/customers.ts`, and `frontend/src/api/invoices.ts`
- [X] T026 [P] [US1] Implement customer entry, line-item entry, and server-total display components in `frontend/src/components/CustomerForm.tsx`, `frontend/src/components/InvoiceForm.tsx`, `frontend/src/components/InvoiceLineItems.tsx`, and `frontend/src/components/InvoiceSummary.tsx`
- [X] T027 [US1] Implement customer/invoice creation flows and routes that show backend validation errors in `frontend/src/pages/CustomersPage.tsx` and `frontend/src/pages/InvoiceCreatePage.tsx`

**Checkpoint**: Customer and Draft creation work end-to-end; calculation, numbering, and input-validation
tests pass.

---

## Phase 4: User Story 2 - Find Customers and Invoices (Priority: P2)

**Goal**: A user can locate customers and invoices and inspect every required invoice detail.

**Independent Test**: With seeded customer/invoice records, open both lists and one invoice detail, then
verify the specified fields, line items, and empty states.

### Tests for User Story 2

- [X] T028 [P] [US2] Write API tests for customer list/detail, invoice list/detail, unknown IDs, and empty collections in `backend/tests/api/test_invoice_reading.py`

### Implementation for User Story 2

- [X] T029 [US2] Add compact invoice-list and complete invoice-detail response mapping in `backend/app/schemas/invoice.py`
- [X] T030 [US2] Add customer list/detail and invoice list/detail service queries with required relationships in `backend/app/services/customers.py` and `backend/app/services/invoices.py`
- [X] T031 [US2] Implement `GET /customers`, `GET /customers/{customerId}`, `GET /invoices`, and `GET /invoices/{invoiceId}` in `backend/app/api/routes/customers.py` and `backend/app/api/routes/invoices.py`
- [X] T032 [US2] Add typed customer/invoice read methods in `frontend/src/api/customers.ts` and `frontend/src/api/invoices.ts`
- [X] T033 [P] [US2] Implement a reusable empty-state component and invoice summary/detail display components in `frontend/src/components/EmptyState.tsx` and `frontend/src/components/InvoiceSummary.tsx`
- [X] T034 [US2] Implement customer list, invoice list, and invoice detail pages in `frontend/src/pages/CustomersPage.tsx`, `frontend/src/pages/InvoicesPage.tsx`, and `frontend/src/pages/InvoiceDetailPage.tsx`
- [X] T035 [US2] Wire list/detail navigation and the new pages into `frontend/src/App.tsx`

**Checkpoint**: Users can retrieve all saved customer and invoice data; empty and unknown-resource cases are
handled and covered by API tests.

---

## Phase 5: User Story 3 - Update Drafts and Invoice Status (Priority: P2)

**Goal**: A user can correct a Draft and apply only the specified status transitions.

**Independent Test**: Edit a Draft and verify recalculation; execute every allowed transition and verify
invalid edits/transitions return a conflict without modifying stored data.

### Tests for User Story 3

- [X] T036 [P] [US3] Write unit tests for the allowed lifecycle graph, rejected transitions, and Draft-only editing in `backend/tests/unit/test_invoice_lifecycle.py`
- [X] T037 [P] [US3] Write API tests for `PUT /invoices/{invoiceId}`, `POST /invoices/{invoiceId}/status`, recalculation, and 409 conflicts in `backend/tests/api/test_invoice_lifecycle.py`

### Implementation for User Story 3

- [X] T038 [US3] Add update and status-command schemas that exclude client-supplied totals and invoice numbers in `backend/app/schemas/invoice.py`
- [X] T039 [US3] Implement Draft-only invoice update, replacement item calculation, and the explicit status-transition graph in `backend/app/services/invoices.py`
- [X] T040 [US3] Implement `PUT /invoices/{invoiceId}` and `POST /invoices/{invoiceId}/status` with 404/409 behavior in `backend/app/api/routes/invoices.py`
- [X] T041 [P] [US3] Add typed update and status API methods in `frontend/src/api/invoices.ts` and status-control component in `frontend/src/components/InvoiceStatusActions.tsx`
- [X] T042 [US3] Implement Draft edit form/page and status-action integration in `frontend/src/pages/InvoiceEditPage.tsx` and `frontend/src/pages/InvoiceDetailPage.tsx`
- [X] T043 [US3] Add edit-route navigation and ensure non-Draft invoices do not expose edit controls in `frontend/src/App.tsx` and `frontend/src/pages/InvoiceDetailPage.tsx`

**Checkpoint**: All allowed lifecycle paths work; invalid lifecycle and editing operations leave invoices
unchanged and are proven by unit/API tests.

---

## Phase 6: User Story 4 - Print an Invoice (Priority: P3)

**Goal**: A user prints a complete, legible invoice from its detail page without creating a PDF/export
service.

**Independent Test**: Open a saved invoice, invoke browser print, and verify its preview contains every
required invoice field and line-item total.

### Tests for User Story 4

- [X] T044 [US4] Add the repeatable print-preview acceptance procedure and field checklist to `specs/001-invoice-management/quickstart.md`

### Implementation for User Story 4

- [X] T045 [US4] Add a print action and a print-specific invoice layout containing all required fields in `frontend/src/pages/InvoiceDetailPage.tsx`
- [X] T046 [US4] Add print media styling that hides navigation/actions and preserves legible invoice totals and line items in `frontend/src/styles/print.css`
- [X] T047 [US4] Load the print stylesheet in `frontend/src/main.tsx`

**Checkpoint**: Print preview is complete and legible while normal application navigation remains unchanged.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Complete verification and ensure the delivered project remains within scope.

- [X] T048 [P] Add concise backend/frontend setup and run instructions to `README.md`
- [X] T049 [P] Add explicit out-of-scope regression checks for authentication, payment, email, recurrence, integrations, multiple currencies, businesses, and tax configuration to `backend/tests/api/test_scope_boundaries.py`
- [X] T050 Run the full backend test suite and frontend production build using the commands in `specs/001-invoice-management/quickstart.md`
- [X] T051 Perform and record the six end-to-end quickstart validation scenarios in `specs/001-invoice-management/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)** has no dependencies.
- **Foundational (Phase 2)** depends on Setup and blocks every user story.
- **US1 (Phase 3)** depends on Foundation and is the MVP.
- **US2 (Phase 4)** depends on US1 because it reads the Customer/Invoice aggregates created by the MVP.
- **US3 (Phase 5)** depends on US1 because it updates its Draft aggregate; it may proceed in parallel with
  US2 after US1 is complete.
- **US4 (Phase 6)** depends on US2 because it prints the invoice detail view.
- **Polish (Phase 7)** depends on all desired story phases.

### User Story Completion Order

```text
Setup → Foundation → US1 (MVP) → ┬→ US2 → US4
                                 └→ US3
                           → Polish
```

### Parallel Opportunities

- T003–T005 can run together after T001.
- T008 can run alongside T006–T007; T010 can start once the database session contract is defined.
- In US1, tests T012–T014 and frontend type/API/component work T024–T026 can proceed in parallel with
  their backend prerequisites respected.
- US2 test T028 and US3 tests T036–T037 can be prepared in parallel after US1's interfaces stabilize.
- After US1, US2 and US3 can be implemented by separate developers; US4 follows completed invoice detail.

## Parallel Example: User Story 1

```text
Task: "Write calculation and rounding tests in backend/tests/unit/test_calculations.py"
Task: "Write invoice-number service tests in backend/tests/unit/test_invoice_service.py"
Task: "Write creation/validation API tests in backend/tests/api/test_invoice_creation.py"

Task: "Define shared frontend contract types in frontend/src/types/customer.ts and frontend/src/types/invoice.ts"
Task: "Implement frontend API client modules in frontend/src/api/client.ts, frontend/src/api/customers.ts, and frontend/src/api/invoices.ts"
```

## Implementation Strategy

### MVP First

1. Complete Setup and Foundation.
2. Complete US1, including its tests.
3. Validate creating a customer and a two-item Draft; verify number and totals.
4. Stop for review before extending to retrieval, lifecycle, and printing.

### Incremental Delivery

1. Deliver US1 as a correct invoice-creation MVP.
2. Add US2 for discoverability and complete invoice detail.
3. Add US3 for Draft corrections and lifecycle control.
4. Add US4 for browser printing, then run cross-cutting checks.

---

## Phase 8: Convergence

- [ ] T052 Add a 100-case varied-valid-invoice calculation conformance test for exact line totals, subtotal, 15% tax, and total in `backend/tests/unit/test_calculations.py` per SC-002 (partial)
- [ ] T053 Add tests for every allowed status transition and cancellation from Draft, Sent, and Overdue in `backend/tests/unit/test_invoice_lifecycle.py` per US3/AC3–AC4 and Constitution V (partial)
- [ ] T054 Align invoice-list API schema/serialization and frontend list types/rendering with the `customer` field in `specs/001-invoice-management/contracts/openapi.yaml` in `backend/app/schemas/invoice.py`, `backend/app/services/invoices.py`, `frontend/src/types/invoice.ts`, and `frontend/src/pages/InvoicesPage.tsx` per plan: REST contract (partial)
- [ ] T055 Add API regression tests for unknown-customer invoice creation and over-precision decimal quantity/unit-price input in `backend/tests/api/test_invoice_creation.py` per plan: API test strategy (partial)
