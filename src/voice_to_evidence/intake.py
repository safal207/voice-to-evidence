"""Intake record model and JSON loading.

Deterministic, dependency-free validation. The intake represents one
AI-agent action described by a human (originally as voice/transcript,
here already normalised to JSON).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

ALLOWED_RECOMMENDATIONS = {"ALLOW", "BLOCK", "ESCALATE"}

REQUIRED_FIELDS = (
    "incident_id",
    "agent_name",
    "workflow",
    "action",
    "permission_boundary",
)

OPTIONAL_STRING_FIELDS = (
    "transcript",
    "reporter",
    "occurred_at",
    "notes",
)


class IntakeValidationError(ValueError):
    """Raised when an intake payload is missing or malformed."""


@dataclass
class IntakeRecord:
    incident_id: str
    agent_name: str
    workflow: str
    action: str
    permission_boundary: str
    transcript: Optional[str] = None
    reporter: Optional[str] = None
    occurred_at: Optional[str] = None
    evidence_before_action: List[str] = field(default_factory=list)
    missing_evidence: List[str] = field(default_factory=list)
    reversibility_risks: List[str] = field(default_factory=list)
    recommendation: Optional[str] = None
    notes: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IntakeRecord":
        if not isinstance(data, dict):
            raise IntakeValidationError("intake payload must be a JSON object")

        missing = [f for f in REQUIRED_FIELDS if not data.get(f)]
        if missing:
            raise IntakeValidationError(
                f"missing required field(s): {', '.join(missing)}"
            )

        for f in REQUIRED_FIELDS:
            if not isinstance(data[f], str):
                raise IntakeValidationError(f"field '{f}' must be a string")

        for optional_string in OPTIONAL_STRING_FIELDS:
            value = data.get(optional_string)
            if value is not None and not isinstance(value, str):
                raise IntakeValidationError(f"field '{optional_string}' must be a string")

        for list_field in ("evidence_before_action", "missing_evidence", "reversibility_risks"):
            value = data.get(list_field, [])
            if value is None:
                continue
            if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
                raise IntakeValidationError(
                    f"field '{list_field}' must be a list of strings"
                )

        recommendation = data.get("recommendation")
        if recommendation is not None:
            if not isinstance(recommendation, str):
                raise IntakeValidationError("recommendation must be a string")
            if recommendation.upper() not in ALLOWED_RECOMMENDATIONS:
                raise IntakeValidationError(
                    f"recommendation must be one of {sorted(ALLOWED_RECOMMENDATIONS)}"
                )
            recommendation = recommendation.upper()

        return cls(
            incident_id=data["incident_id"],
            agent_name=data["agent_name"],
            workflow=data["workflow"],
            action=data["action"],
            permission_boundary=data["permission_boundary"],
            transcript=data.get("transcript"),
            reporter=data.get("reporter"),
            occurred_at=data.get("occurred_at"),
            evidence_before_action=list(data.get("evidence_before_action") or []),
            missing_evidence=list(data.get("missing_evidence") or []),
            reversibility_risks=list(data.get("reversibility_risks") or []),
            recommendation=recommendation,
            notes=data.get("notes"),
        )


def load_intake(payload: str) -> IntakeRecord:
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as e:
        raise IntakeValidationError(f"invalid JSON: {e}") from e
    return IntakeRecord.from_dict(data)


def load_intake_from_file(path: str | Path) -> IntakeRecord:
    p = Path(path)
    if not p.exists():
        raise IntakeValidationError(f"intake file not found: {p}")
    return load_intake(p.read_text(encoding="utf-8"))
