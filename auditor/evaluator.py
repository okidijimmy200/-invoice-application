from audit_models import Evidence, VerificationResult


def evaluate(
    obligation_id: str,
    expected,
    observed,
    source: str,
) -> VerificationResult:

    evidence = Evidence(
        obligation_id=obligation_id,
        expected=expected,
        observed=observed,
        source=source,
    )

    if observed is None:
        return VerificationResult(
            obligation_id=obligation_id,
            status="UNVERIFIED",
            evidence=evidence,
            reason="No observable runtime result was available.",
        )

    if expected == observed:
        return VerificationResult(
            obligation_id=obligation_id,
            status="PASS",
            evidence=evidence,
            reason="Observed runtime behavior matched the independent expectation.",
        )

    return VerificationResult(
        obligation_id=obligation_id,
        status="FAIL",
        evidence=evidence,
        reason="Observed runtime behavior contradicted the independent expectation.",
    )