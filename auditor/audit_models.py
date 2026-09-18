from dataclasses import dataclass
from typing import Literal


VerificationMethod = Literal[
    "api",
    "command",
    "process",
    "static",
]


@dataclass
class VerificationObligation:
    id: str
    requirement_id: str
    description: str
    method: VerificationMethod
    expected: str


@dataclass
class PlannedObligation:
    description: str
    method: VerificationMethod
    expected: str

from typing import Any


@dataclass
class Evidence:
    obligation_id: str
    expected: Any
    observed: Any
    source: str


@dataclass
class VerificationResult:
    obligation_id: str
    status: Literal["PASS", "FAIL", "UNVERIFIED"]
    evidence: Evidence | None
    reason: str