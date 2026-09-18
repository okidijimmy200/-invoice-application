from pathlib import Path

from audit_models import VerificationResult


def generate_report(
    requirement: dict,
    results: list[VerificationResult],
    output_file: Path,
) -> None:
    lines = [
        "# Independent Runtime Audit Report",
        "",
        f"## Requirement {requirement['id']}",
        "",
        requirement["text"],
        "",
        "## Verification Results",
        "",
    ]

    for result in results:
        lines.extend(
            [
                f"### {result.obligation_id} — {result.status}",
                "",
            ]
        )

        if result.evidence is not None:
            lines.extend(
                [
                    f"- **Source:** {result.evidence.source}",
                    f"- **Expected:** `{result.evidence.expected}`",
                    f"- **Observed:** `{result.evidence.observed}`",
                ]
            )
        else:
            lines.append(
                "- **Source:** No executable evidence collected"
            )

        lines.extend(
            [
                f"- **Reason:** {result.reason}",
                "",
            ]
        )

    statuses = [result.status for result in results]

    if "FAIL" in statuses:
        overall_status = "FAIL"
    elif "UNVERIFIED" in statuses:
        overall_status = "UNVERIFIED"
    elif statuses and all(status == "PASS" for status in statuses):
        overall_status = "PASS"
    else:
        overall_status = "UNVERIFIED"

    lines.extend(
        [
            "## Requirement Result",
            "",
            f"**{requirement['id']}: {overall_status}**",
            "",
        ]
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )