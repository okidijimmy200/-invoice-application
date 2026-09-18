# Independent Runtime Audit Report

## Requirement AC-003

Invoice calculations must correctly derive line totals, subtotal, 15% tax, and total.

## Verification Results

### VO-003-01 — UNVERIFIED

- **Source:** No executable evidence collected
- **Reason:** The planner produced this as a setup action rather than an independently evaluated assertion.

### VO-003-02 — PASS

- **Source:** runtime-api
- **Expected:** `['200.00', '50.00']`
- **Observed:** `['200.00', '50.00']`
- **Reason:** Observed runtime behavior matched the independent expectation.

### VO-003-03 — PASS

- **Source:** runtime-api
- **Expected:** `250.00`
- **Observed:** `250.00`
- **Reason:** Observed runtime behavior matched the independent expectation.

### VO-003-04 — PASS

- **Source:** runtime-api
- **Expected:** `37.50`
- **Observed:** `37.50`
- **Reason:** Observed runtime behavior matched the independent expectation.

### VO-003-05 — PASS

- **Source:** runtime-api
- **Expected:** `287.50`
- **Observed:** `287.50`
- **Reason:** Observed runtime behavior matched the independent expectation.

## Requirement Result

**AC-003: UNVERIFIED**
