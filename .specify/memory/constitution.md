<!--
Sync Impact Report
- Version change: template → 1.0.0
- Modified principles: none (initial adoption)
- Added sections: Core Principles, Initial Scope, Development Workflow, Governance
- Removed sections: none
- Follow-up TODOs: none
-->
# Invoice Management Application Constitution

## Core Principles

### I. Simplicity First
The application MUST use the simplest readable solution that meets the stated requirement.
New abstractions, infrastructure, patterns, or layers MUST have a concrete, present need; speculative
generality is prohibited. Rationale: a deliberately small first release is easier to understand, verify,
and evolve.

### II. Clean Separation
Business logic, API logic, database access, and UI concerns MUST remain in distinct, clearly named
modules or layers. Business rules MUST NOT depend directly on transport, persistence, or presentation
details. Rationale: separation makes changes local and keeps the invoice domain independently testable.

### III. Correctness
Invoice calculations for quantities, unit prices, line totals, invoice totals, and payment status MUST be
deterministic. The implementation MUST define and consistently apply its monetary precision and rounding
rules. Changes to these rules require automated tests covering normal and boundary cases. Rationale:
financial records must be reliable and reproducible.

### IV. Validation at the Boundary
API boundaries MUST validate all user-controlled input before it reaches business logic or persistence.
The system MUST reject invalid invoice data, including malformed values, invalid quantities or prices, and
inconsistent payment states, with clear errors. Rationale: invalid financial data is costly to repair after
storage.

### V. Testability
Important business rules MUST have automated tests. At minimum, tests MUST cover invoice total
calculation, quantity and price validation, and payment-status transitions; new or changed domain rules
MUST include corresponding tests. Rationale: tests provide durable proof of financial correctness.

### VI. Maintainability
Code MUST favor clear names, small focused functions, and conventional project structure. Duplication or
complexity MAY be refactored only when doing so improves clarity without violating Simplicity First.
Rationale: maintainable code lowers the cost and risk of future changes.

### VII. Minimal Dependencies
A dependency MAY be introduced only when it provides clear value that outweighs its maintenance,
security, and operational cost. Each new dependency MUST have a defined purpose; existing platform or
project capabilities SHOULD be preferred when sufficient. Rationale: a small dependency surface keeps
the application understandable and resilient.

## Initial Scope

The first version MUST remain intentionally small and focused on core invoice management. It MUST NOT
include authentication, payment processing, email delivery, recurring invoices, accounting integrations,
or other features absent from the initial specification. Any proposal to add a deferred capability requires
an explicit specification and a constitution amendment when it changes this scope.

## Development Workflow

Before implementation, work MUST identify the affected boundary, business-rule, persistence, and UI
responsibilities. Pull requests and reviews MUST verify separation of concerns, boundary validation,
deterministic invoice behavior, relevant automated tests, and justification for each new dependency.
Tests for material business-rule changes MUST pass before merge.

## Governance

This constitution supersedes conflicting project conventions and implementation preferences. Amendments
MUST be documented in this file, include a rationale and impact on affected work, and receive project
maintainer approval. Versioning follows semantic rules: MAJOR for incompatible principle removals or
redefinitions, MINOR for new principles or material governance expansion, and PATCH for clarifications
that do not change governance intent. Every pull request review MUST assess compliance; deviations
require documented, maintainer-approved justification.

**Version**: 1.0.0 | **Ratified**: 2026-09-06 | **Last Amended**: 2026-09-06
