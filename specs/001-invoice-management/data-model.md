# Data Model: Invoice Management

## Conventions

- Database primary keys are internal integers and external API IDs.
- USD monetary fields are non-negative integer cents; API responses use fixed two-place strings.
- Quantity is stored as integer thousandths and exposed as a decimal string with up to three places.
- The calculation service alone derives and persists line totals, subtotal, tax, and total.

## Customer

| Field | Type | Rules |
|-------|------|-------|
| id | integer | Primary key. |
| name | text | Required, trimmed, non-blank. |
| phone | text | Required, trimmed, non-blank. |
| email | text | Required, valid email format. |
| address | text | Required, trimmed, non-blank. |

One Customer has zero or more Invoices. Every Invoice references one existing Customer. Customer editing
and deletion are outside the first-release scope.

## Invoice

| Field | Type | Rules |
|-------|------|-------|
| id | integer | `INTEGER PRIMARY KEY AUTOINCREMENT`; never repurposed. |
| invoice_number | text | Required, unique, immutable; `INV-` plus id padded to at least four digits. |
| customer_id | integer | Required foreign key to Customer. |
| issue_date | date | Required. |
| due_date | date | Required; not earlier than issue_date. |
| status | text enum | Draft, Sent, Paid, Overdue, or Cancelled; new records are Draft. |
| subtotal_cents | integer | Derived non-negative sum of lines. |
| tax_cents | integer | Derived 15% tax rounded half up. |
| total_cents | integer | Derived subtotal plus tax. |
| notes | text | Optional; blank allowed. |
| payment_terms | text | Optional; blank allowed. |

Creation, item replacement, total calculation, and number assignment run in one transaction.

### Lifecycle

| Current status | Allowed next status |
|----------------|---------------------|
| Draft | Sent, Cancelled |
| Sent | Paid, Overdue, Cancelled |
| Overdue | Cancelled |
| Paid | None |
| Cancelled | None |

Only Draft invoices are editable. A rejected edit or transition leaves stored data unchanged.

## Invoice Item

| Field | Type | Rules |
|-------|------|-------|
| id | integer | Primary key. |
| invoice_id | integer | Required foreign key to Invoice. |
| description | text | Required, trimmed, non-blank. |
| quantity_millis | integer | Required, greater than zero; represents quantity × 1,000. |
| unit_price_cents | integer | Required and zero or greater. |
| line_total_cents | integer | Derived, rounded half up to cents. |

## Calculation Rules

1. Convert `quantity_millis / 1000` and `unit_price_cents / 100` to Decimal values.
2. `line_total = quantize(quantity × unit_price, 0.01, ROUND_HALF_UP)`.
3. `subtotal = sum(line_total)`.
4. `tax = quantize(subtotal × 0.15, 0.01, ROUND_HALF_UP)`.
5. `total = subtotal + tax`.

All cents values are persisted atomically with the invoice and items.
