# Invoice Management Application

A small web application for creating customers and USD invoices. The project was created with
**Spec Kit Spec-Driven Development (SDD)**: define the rules, specify the user outcomes, plan the design,
generate tasks, implement, and compare the result back to its original intent.

## Product overview

- Create and view customers with name, phone, email, and address.
- Create Draft invoices with generated numbers such as `INV-0001`.
- Calculate line totals, subtotal, fixed 15% tax, and final total in USD.
- Store money as integer cents and calculate it with backend `Decimal` logic to avoid floating-point error.
- List and inspect invoices, edit Drafts only, and enforce the supported payment-status lifecycle.
- Print a complete invoice using the browser print view.

Version 1 deliberately excludes authentication, payments, email delivery, recurring invoices, accounting
integrations, multiple currencies, multiple businesses, and configurable tax rules.

## Technology

| Area | Technology |
|---|---|
| Backend | Python 3.11+, FastAPI, Pydantic, SQLAlchemy |
| Database | SQLite |
| Tests | pytest and FastAPI test client |
| Frontend | React, TypeScript, Vite, React Router |

The backend is the source of truth for validation, calculations, invoice numbers, and status transitions.
The frontend provides forms, lists, details, and printing through the REST API.

## Project structure

```text
backend/                         FastAPI application and automated tests
frontend/                        React/Vite application
specs/001-invoice-management/    Spec Kit SDD artifacts
├── spec.md                      Requirements and acceptance scenarios
├── plan.md                      Architecture and implementation plan
├── research.md                  Technical decisions and alternatives
├── data-model.md                Entities, storage, and status rules
├── contracts/openapi.yaml       REST API contract
├── tasks.md                     Ordered implementation checklist
└── quickstart.md                Setup and validation guide
.specify/memory/constitution.md  Engineering principles and governance
```

## Spec Kit SDD workflow

The project is traceable from its business goals to its implementation through the following commands.

| Command | Purpose | Project result |
|---|---|---|
| `$speckit-constitution` | Establish project rules and governance. | Defined simplicity, separation of concerns, correctness, validation, testability, maintainability, minimal dependencies, and a small first-release scope. |
| `$speckit-specify` | Convert the product request into testable requirements. | Produced user stories, acceptance scenarios, functional requirements, edge cases, success criteria, and a quality checklist in [spec.md](specs/001-invoice-management/spec.md). |
| `$speckit-plan` | Design the technical approach before implementation. | Defined the FastAPI/React monorepo, integer-cent and Decimal money policy, SQLite model, REST API, testing strategy, and setup in [plan.md](specs/001-invoice-management/plan.md). |
| `$speckit-tasks` | Produce dependency-ordered, executable work. | Created tasks for setup, shared foundations, each user story, printing, tests, and validation in [tasks.md](specs/001-invoice-management/tasks.md). |
| `$speckit-implement` | Build the planned work and mark tasks complete. | Implemented the backend, frontend, automated tests, print styling, and run instructions. |
| `$speckit-converge` | Assess the code against the Spec Kit artifacts. | Added Phase 8 follow-ups for remaining test coverage and REST-contract alignment. |

This is the value of SDD in this project: implementation is not disconnected from the original request.
The specification, plan, data model, API contract, task list, and validation guide remain reviewable source
artifacts alongside the code.

## Run locally

### Backend

```sh
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`; API documentation is available at
`http://127.0.0.1:8000/docs`.

### Frontend

In another terminal:

```sh
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal. Its development server proxies `/api/v1` requests to the backend.

## Validate the project

```sh
cd backend
.venv/bin/pytest

cd ../frontend
npm run build
```

The test suite covers invoice calculations, 15% tax, validation, invoice numbering, Draft-only editing,
status conflicts, and selected API edge cases. For end-to-end checks, use
[quickstart.md](specs/001-invoice-management/quickstart.md). For planned and remaining work, see
[tasks.md](specs/001-invoice-management/tasks.md).

## API overview

The REST API is versioned under `/api/v1`.

- `POST`, `GET /customers` and `GET /customers/{customerId}`
- `POST`, `GET /invoices` and `GET`, `PUT /invoices/{invoiceId}`
- `POST /invoices/{invoiceId}/status`

See [openapi.yaml](specs/001-invoice-management/contracts/openapi.yaml) for request and response shapes.
