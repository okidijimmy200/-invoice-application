# Implementation Plan: Invoice Management

**Branch**: `001-invoice-management` | **Date**: 2026-09-06 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-invoice-management/spec.md`

## Summary

Build a deliberately small single-business invoice-management web application. A React/TypeScript
frontend creates and displays customers and invoices; a FastAPI REST backend owns validation,
deterministic USD calculation, invoice numbering, and lifecycle decisions. SQLAlchemy persists records in
SQLite. Money is accepted and returned as decimal strings, calculated with `Decimal`, and stored as
integer cents to eliminate binary floating-point error.

## Technical Context

**Language/Version**: Python 3.11+; TypeScript with React

**Primary Dependencies**: FastAPI, Pydantic, SQLAlchemy, pytest; React, Vite, React Router

**Storage**: SQLite; all USD money is integer cents

**Testing**: pytest unit and API integration tests; frontend type check and production build

**Target Platform**: Modern desktop browsers; local development on macOS, Linux, or Windows

**Project Type**: Web application monorepo with independently runnable backend and frontend

**Performance Goals**: List and detail views with up to 100 invoices are usable within one second in local
validation. A user completes customer plus two-line-item invoice entry in under three minutes.

**Constraints**: USD only; fixed 15% tax; no floating-point financial arithmetic; backend is the source
of truth; no authentication, payments, email, recurring invoices, accounting integrations, multi-currency,
multi-business, or advanced tax configuration.

**Scale/Scope**: One internal-user context, one business, local SQLite storage, invoice lifecycle, and
browser print preview.

## Constitution Check

| Gate | Plan response | Status |
|------|---------------|--------|
| Simplicity First | Two apps are required by the requested stack. Each uses conventional routes, services, and persistence without repository patterns, event buses, UI frameworks, or state libraries. | PASS |
| Clean Separation | Routes adapt HTTP; Pydantic schemas validate I/O; services own domain rules; models persist records; React pages orchestrate UI and API modules own transport. | PASS |
| Correctness | The calculation service uses explicit `Decimal` conversion and `ROUND_HALF_UP`, persists cents, and alone computes totals. | PASS |
| Validation | Pydantic validates shape and simple constraints; service methods enforce customer existence, editable state, transitions, and numbering invariants. | PASS |
| Testability | Pure calculation and transition functions receive focused pytest coverage; API tests use isolated SQLite databases. | PASS |
| Maintainability and Dependencies | Tree is conventional and small. React Router is the only added frontend runtime dependency beyond React/Vite. | PASS |
| Initial Scope | The model, contracts, and UI omit every explicitly deferred capability. | PASS |

**Post-design re-check**: PASS. Design keeps financial and lifecycle logic in backend services and adds no
scope-expanding infrastructure.

## Project Structure

### Documentation (this feature)

```text
specs/001-invoice-management/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── openapi.yaml
└── tasks.md                 # Created later by $speckit-tasks
```

### Source Code (repository root)

```text
backend/
├── .venv/                   # Ignored local Python virtual environment
├── requirements.txt
├── app/
│   ├── main.py
│   ├── api/routes/{customers,invoices}.py
│   ├── db/{base,session}.py
│   ├── models/{customer,invoice,invoice_item}.py
│   ├── schemas/{customer,invoice}.py
│   └── services/{calculations,customers,invoices}.py
└── tests/
    ├── conftest.py
    ├── unit/{test_calculations,test_invoice_service}.py
    └── api/{test_customers,test_invoices}.py

frontend/
├── package.json
├── vite.config.ts
└── src/
    ├── api/{client,customers,invoices}.ts
    ├── components/{CustomerForm,EmptyState,InvoiceForm,InvoiceLineItems,InvoiceStatusActions,InvoiceSummary}.tsx
    ├── pages/{CustomersPage,InvoiceCreatePage,InvoiceDetailPage,InvoiceEditPage,InvoicesPage}.tsx
    ├── styles/print.css
    ├── types/{customer,invoice}.ts
    ├── App.tsx
    └── main.tsx
```

**Structure Decision**: This is the requested simple monorepo. Backend layers make invariants testable
without HTTP or SQLite. Frontend separates page orchestration, reusable UI, API access, and contract types.
The UI displays backend-computed totals and prints with CSS plus `window.print()`, not a PDF service.

## Architecture and Requirement Mapping

| Requirement area | Design decision |
|------------------|-----------------|
| FR-001–002 | Customer schemas validate required contact details and email. Customer routes/service expose create, list, and detail. |
| FR-003–009, FR-016 | Invoice schemas validate dates/items. Invoice service verifies the customer, derives totals, and persists the aggregate atomically. |
| FR-004 | SQLite `INTEGER PRIMARY KEY AUTOINCREMENT` supplies internal invoice IDs. One transaction inserts and flushes, derives `INV-{id:04d}`, stores it under a unique constraint, then commits. No client number or `MAX()` query is used. |
| FR-007–008 | `calculations.py` constructs Decimal from strings, uses `ROUND_HALF_UP`, rounds each line, sums lines, then rounds 15% tax. API returns fixed two-place strings. |
| FR-010–011 | Separate list/detail schemas provide a compact list and complete invoice detail. |
| FR-012–014 | Invoice service holds the allowed status graph and rejects non-Draft updates. Routes map domain conflicts to HTTP errors. |
| FR-015 | Detail page exposes all print fields and supplies print styling/action. |
| FR-017 | No routes, data models, UI, or dependencies for excluded functionality. |

## Development and Test Strategy

1. Create `backend/.venv` with Python 3.11+ and install only FastAPI, SQLAlchemy, Pydantic, Uvicorn,
   pytest, and HTTP test support. Ignore `.venv`, SQLite files, and frontend build output.
2. Provide pytest fixtures for a temporary SQLite database and FastAPI test client.
3. Unit-test calculations: multi-line totals, 15% tax, zero-price items, fractional quantity rounding,
   two-place output, and changed Decimal context. Unit-test unique/no-reuse numbers, transitions, and
   Draft-only edits.
4. API-test required customer data/email, missing customer/item, invalid dates, blank descriptions,
   invalid quantity/price, unknown IDs, empty collections, generated totals, and `404`/`409` errors.
5. Build the frontend from the contract. Forms show server validation errors and never submit totals as
   authoritative. Validate with TypeScript/Vite build plus quickstart manual flows.

## Complexity Tracking

No constitution violations require justification.
