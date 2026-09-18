from audit_models import VerificationObligation


def build_sample_obligations(requirement: dict) -> list[VerificationObligation]:

    requirement_id = requirement["id"]

    if requirement_id != "AC-003":
        raise ValueError(
            f"Sample obligation builder only supports AC-003, got {requirement_id}"
        )
    return [
        VerificationObligation(
            id="VO-003-01",
            requirement_id=requirement_id,
            description="Verify each invoice line total equals quantity multiplied by unit price.",
            method="api",
            expected="For known line items, each returned line total matches quantity × unit price.",
        ),
        VerificationObligation(
            id="VO-003-02",
            requirement_id=requirement_id,
            description="Verify invoice subtotal equals the sum of all line totals.",
            method="api",
            expected="Returned subtotal equals the sum of returned line totals.",
        ),
        VerificationObligation(
            id="VO-003-03",
            requirement_id=requirement_id,
            description="Verify invoice tax equals 15% of subtotal.",
            method="api",
            expected="Returned tax equals subtotal × 0.15.",
        ),
        VerificationObligation(
            id="VO-003-04",
            requirement_id="AC-003",
            description="Verify invoice total equals subtotal plus tax.",
            method="api",
            expected="Returned total equals subtotal + tax.",
        ),
    ]