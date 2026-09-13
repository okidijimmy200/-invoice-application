# Research: Invoice Management

## Deterministic USD Calculations

**Decision**: Use Python `Decimal` only at the API/service boundary, constructed from strings or integers.
Define `CENT = Decimal("0.01")`, `TAX_RATE = Decimal("0.15")`, and `ROUND_HALF_UP`. Round each line to
cents; subtotal is the sum of rounded lines; tax is rounded `subtotal × 0.15`; total is their sum. Store
all money as integer cents and serialize it as fixed two-place USD strings.

**Rationale**: This follows the specified formula order, avoids binary floats, and is deterministic on
SQLite. Explicit rounding avoids dependence on a mutable Decimal context.

**Alternatives considered**: SQLite `REAL` and floats are rejected for binary rounding error. SQLite
`NUMERIC` plus Decimal is less predictable with SQLite adapters. Decimal strings in storage are exact but
make numeric constraints less clear than integer cents.

## Quantity and Input Validation

**Decision**: Accept `unit_price` and `quantity` as decimal strings. Permit prices with at most two places
and quantities with at most three; persist quantity as scaled integer thousandths. Require finite values,
price at least zero, quantity greater than zero, a non-blank description, and at least one item. Pydantic
validates request boundaries; services reassert domain invariants.

**Rationale**: Fractional quantities are supported without a float or arbitrary precision storage scheme.

**Alternatives considered**: Integer-only quantities restrict the specification. Unlimited precision makes
validation and persistence unnecessarily complex.

## Invoice Number Generation

**Decision**: Use SQLite `INTEGER PRIMARY KEY AUTOINCREMENT` as the internal ID and a unique, immutable
`invoice_number`. In one service transaction, insert and flush the invoice, set
`invoice_number = f"INV-{id:04d}"`, and commit. Never return a success before commit.

**Rationale**: SQLite does not reuse committed AUTOINCREMENT IDs, including after deletion. Formatting a
database-assigned ID is deterministic and avoids racy/reusable `MAX()+1` numbering. The unique constraint
is defense in depth. Gaps after failed transactions are permitted because numbers must never be reused,
not gaplessly reserved.

**Alternatives considered**: A `MAX()` query races and can reuse values. A separate sequence table adds a
coordination record without value for this single SQLite application. UUIDs cannot meet the required format.

## REST Boundary and Errors

**Decision**: Provide `/api/v1` JSON resources for customers and invoices, with a command-style status
endpoint. Use `422` for input errors, `404` for unknown resources, and `409` for non-Draft edit or invalid
transition conflicts. Domain errors expose a stable code and readable message.

**Rationale**: The small surface maps exactly to the feature and a separate status command prevents
arbitrary updates from bypassing the state graph.

**Alternatives considered**: Generic PATCH accepting status weakens lifecycle protection. Server PDF
generation is beyond the print-preview scope.

## Frontend Integration

**Decision**: Use a fetch wrapper and resource API modules with TypeScript contract types. React pages
compose reusable form/display components; React Router handles the required views. Vite proxies relative
`/api/v1` requests during development, with explicit FastAPI CORS origins for direct use.

**Rationale**: This separates transport, page orchestration, and UI without a state library. Backend totals
remain authoritative and printing remains the browser's responsibility.

**Alternatives considered**: A giant component is hard to maintain. A component framework, global state
library, browser E2E suite, and wildcard CORS add first-release complexity without clear value.
