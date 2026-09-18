from openai import OpenAI
from pydantic import BaseModel
from typing import Literal

from audit_models import VerificationObligation


client = OpenAI()


class PlannedObligationOutput(BaseModel):
    description: str
    method: Literal["api", "command", "process", "static"]
    expected: str


class VerificationPlanOutput(BaseModel):
    obligations: list[PlannedObligationOutput]


def plan_verification(requirement: dict) -> list[VerificationObligation]:
    requirement_id = requirement["id"]
    requirement_text = requirement["text"]

    response = client.responses.parse(
        model="gpt-5.6-luna",
        input=[
            {
                "role": "system",
                "content": (
                    "You are the verification planner for an independent "
                    "software auditor. Decompose an acceptance requirement "
                    "into the smallest meaningful verification obligations. "
                    "Each obligation must describe one observable claim that "
                    "can be independently verified. "
                    "\n\n"
                    "Available verification methods:\n"
                    "- api: verify observable application behavior through HTTP APIs.\n"
                    "- command: execute a finite command such as tests or a build.\n"
                    "- process: start or inspect a long-running application process.\n"
                    "- static: inspect source code or configuration when runtime "
                    "verification is not appropriate.\n"
                    "\n"
                    "Prefer direct runtime evidence over static inspection. "
                    "Use api for business behavior exposed through an API. "
                    "Use process only for process-level claims such as whether an "
                    "application can start and remain running. "
                    "Do not assume browser automation is available. "
                    "Do not create an obligation merely to inspect a UI unless the "
                    "requirement specifically requires UI behavior. "
                    "\n\n"
                    "Do not decide PASS or FAIL. "
                    "Do not invent requirement IDs or verification IDs."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Requirement ID: {requirement_id}\n"
                    f"Requirement:\n{requirement_text}"
                ),
            },
        ],
        text_format=VerificationPlanOutput,
    )

    plan = response.output_parsed

    if plan is None:
        raise RuntimeError(
            f"Planner returned no structured output for {requirement_id}"
        )

    requirement_number = requirement_id.split("-")[1]

    obligations = []

    for index, planned in enumerate(plan.obligations, start=1):
        obligations.append(
            VerificationObligation(
                id=f"VO-{requirement_number}-{index:02d}",
                requirement_id=requirement_id,
                description=planned.description,
                method=planned.method,
                expected=planned.expected,
            )
        )

    return obligations