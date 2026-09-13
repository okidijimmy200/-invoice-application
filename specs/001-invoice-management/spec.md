# Feature Specification: Invoice Management

**Feature Branch**: `001-invoice-management`

**Created**: 2026-09-06

**Status**: Draft

**Input**: User description: "Build a simple invoice management application for customers and invoices."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create a Customer and Draft Invoice (Priority: P1)

A user creates a customer with complete contact details, creates a draft invoice for that customer, adds
line items, and sees accurate USD totals before saving the invoice.

**Why this priority**: Creating a correct draft invoice is the core value of the application and enables
all later invoice actions.

**Independent Test**: A user can create a customer, create a draft containing two line items, and verify
the generated number, customer, dates, totals, notes, and payment terms without using any other flow.

**Acceptance Scenarios**:

1. **Given** no matching customer exists, **When** the user provides a name, phone, email, and address,
   **Then** the system creates and displays the customer.
2. **Given** a customer exists, **When** the user creates an invoice with issue date, due date, at least
   one valid line item, notes, and payment terms, **Then** the system saves it as Draft with the next
   invoice number in the `INV-0001` sequence and displays its calculated totals in USD.
3. **Given** a draft invoice contains line items, **When** the user views the invoice, **Then** each line
   total equals quantity multiplied by unit price, subtotal equals all line totals, tax equals 15% of the
   subtotal, and total equals subtotal plus tax.

---

### User Story 2 - Find Customers and Invoices (Priority: P2)

A user views customers, views the invoice list, and opens an individual invoice to find its customer,
status, dates, line items, and totals.

**Why this priority**: Users need to retrieve their records and understand an invoice after it is created.

**Independent Test**: With saved customer and invoice records, a user can open the customer list, invoice
list, and a selected invoice, then confirm all saved details are visible.

**Acceptance Scenarios**:

1. **Given** one or more customers exist, **When** the user views customers, **Then** each customer's
   name, phone, email, and address are displayed.
2. **Given** one or more invoices exist, **When** the user views invoices, **Then** each invoice's number,
   customer, issue date, due date, status, and total are displayed.
3. **Given** an invoice exists, **When** the user opens it, **Then** all required invoice fields and its
   line items are displayed.

---

### User Story 3 - Update Drafts and Invoice Status (Priority: P2)

A user corrects a draft invoice before sending it and advances or cancels invoices according to the
supported lifecycle.

**Why this priority**: A usable invoice workflow requires correction before sending and reliable tracking
of the invoice's payment state.

**Independent Test**: A user can edit a draft, send it, mark it Paid or Overdue, and cancel an eligible
invoice while invalid edits and transitions are refused.

**Acceptance Scenarios**:

1. **Given** an invoice is Draft, **When** the user edits its permitted details or line items with valid
   values, **Then** the invoice is updated and its totals are recalculated.
2. **Given** an invoice is Draft, **When** the user marks it Sent, **Then** its status becomes Sent.
3. **Given** an invoice is Sent, **When** the user marks it Paid or Overdue, **Then** its status becomes
   Paid or Overdue respectively.
4. **Given** an invoice is Draft, Sent, or Overdue, **When** the user cancels it, **Then** its status
   becomes Cancelled.
5. **Given** a requested status change or edit is not allowed, **When** the user submits it, **Then** the
   system rejects the change and leaves the invoice unchanged.

---

### User Story 4 - Print an Invoice (Priority: P3)

A user opens any invoice and produces a print-ready representation that clearly communicates the invoice
to its customer.

**Why this priority**: Printing is needed to share a completed invoice without adding email delivery or
online payment features.

**Independent Test**: A user opens a saved invoice and invokes print, then verifies the print preview
contains its number, dates, customer information, status, line items, subtotal, tax, total, notes, and
payment terms.

**Acceptance Scenarios**:

1. **Given** an invoice exists, **When** the user prints it, **Then** the print-ready output contains all
   invoice fields and line-item totals in a legible layout.

### Edge Cases

- The system rejects customer creation or updates when any required contact field is blank or the email
  is not in a valid email format.
- The system rejects an invoice without a customer or line items, with a due date before its issue date,
  or with blank item descriptions, non-positive quantities, or negative unit prices.
- The first invoice number is `INV-0001`; each newly created invoice receives the next unused sequential
  number, and a number is never reused after an invoice is created.
- Monetary totals are rounded consistently to two decimal places in USD; calculations preserve the stated
  formula before display rounding.
- A Paid or Cancelled invoice cannot move to another status, and a non-Draft invoice cannot be edited.
- When no customers or invoices exist, their respective lists display an empty-state message rather than
  stale or placeholder records.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST allow users to create and view customers with name, phone, email, and
  address; all four fields are required.
- **FR-002**: The system MUST validate customer email addresses and reject invalid customer data with a
  clear error.
- **FR-003**: The system MUST allow users to create an invoice for an existing customer.
- **FR-004**: The system MUST assign each newly created invoice the next globally sequential number in
  the format `INV-0001`, `INV-0002`, and so on, without reusing assigned numbers.
- **FR-005**: The system MUST create each new invoice with status Draft and record its issue date, due
  date, customer, line items, notes, and payment terms.
- **FR-006**: The system MUST require at least one invoice item; each item MUST have a non-blank
  description, a quantity greater than zero, and a unit price of zero or greater.
- **FR-007**: The system MUST calculate each line total as quantity × unit price, subtotal as the sum of
  line totals, tax as 15% of subtotal, and total as subtotal + tax, all in USD.
- **FR-008**: The system MUST round displayed USD monetary amounts consistently to two decimal places.
- **FR-009**: The system MUST reject invoice data with a missing customer, missing required dates, or a
  due date earlier than the issue date.
- **FR-010**: The system MUST allow users to view a list of invoices showing invoice number, customer,
  issue date, due date, status, and total.
- **FR-011**: The system MUST allow users to view an individual invoice with every required invoice field
  and all item-level details.
- **FR-012**: The system MUST allow users to edit only Draft invoices and MUST recalculate totals after
  a valid edit.
- **FR-013**: The system MUST support only these status transitions: Draft → Sent; Sent → Paid; Sent →
  Overdue; and Draft, Sent, or Overdue → Cancelled.
- **FR-014**: The system MUST reject unsupported status transitions and preserve the existing invoice
  state when a transition is rejected.
- **FR-015**: The system MUST provide a print-ready view of an invoice containing its number, dates,
  customer, status, line items, totals, notes, and payment terms.
- **FR-016**: The system MUST use USD as the sole currency and a single, non-configurable 15% tax rate
  for all invoices.
- **FR-017**: The first release MUST NOT include authentication, online payments, email delivery,
  recurring invoices, accounting integrations, multiple currencies, multiple businesses, or advanced tax
  configuration.

### Key Entities *(include if feature involves data)*

- **Customer**: A recipient of invoices, identified by name and represented with phone, email, and
  address contact details.
- **Invoice**: A billing record belonging to one customer, with a generated number, dates, status,
  monetary totals, notes, payment terms, and one or more line items.
- **Invoice Item**: A billed entry within one invoice containing a description, quantity, unit price, and
  calculated line total.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can create a customer and a valid draft invoice with two line items in under three
  minutes in a representative usability test.
- **SC-002**: For 100 invoices with varied valid line items, displayed line totals, subtotal, tax, and
  total match the specified formulas and 15% tax rate in 100% of test cases.
- **SC-003**: In representative usability testing, at least 90% of users can locate a known invoice from
  the invoice list and open its details on their first attempt.
- **SC-004**: In status-lifecycle tests, 100% of allowed transitions succeed and 100% of disallowed
  transitions are refused without changing the stored status.
- **SC-005**: In print-preview tests, 100% of sampled invoices show all required invoice fields and
  line-item totals before printing.

## Assumptions

- The first release serves a single internal user context and therefore does not need authentication or
  roles.
- A customer must exist before an invoice can be created; customer editing and deletion are outside the
  requested first-release scope.
- An invoice's issue date and due date are entered by the user; their only required chronological rule is
  that the due date is not earlier than the issue date.
- Zero-priced line items are permitted for discounts or complimentary items, while quantities remain
  strictly positive.
- Notes and payment terms may be blank unless a user supplies them.
- Printing means producing a browser or system print preview; electronic delivery and payment collection
  are out of scope.
