"""Deterministic transcript-to-intake draft extraction.

This module intentionally avoids LLMs, network calls, and probabilistic parsing.
It extracts a draft IntakeRecord from a lightly structured transcript using
simple section labels. Raw natural-language extraction belongs in a later
optional voice/LLM layer.
"""

from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, Iterable

from voice_to_evidence.intake import IntakeRecord, IntakeValidationError

SECTION_ALIASES = {
    "workflow": "workflow",
    "action": "action",
    "permission": "permission_boundary",
    "permission boundary": "permission_boundary",
    "evidence": "evidence_before_action",
    "evidence before action": "evidence_before_action",
    "missing evidence": "missing_evidence",
    "missing": "missing_evidence",
    "risks": "reversibility_risks",
    "reversibility risks": "reversibility_risks",
    "recommendation": "recommendation",
    "notes": "notes",
}

LIST_FIELDS = {
    "evidence_before_action",
    "missing_evidence",
    "reversibility_risks",
}

REQUIRED_EXTRACTED_FIELDS = {
    "workflow",
    "action",
    "permission_boundary",
}


def _normalise_label(label: str) -> str | None:
    return SECTION_ALIASES.get(label.strip().lower())


def _clean_value(value: str) -> str:
    value = value.strip()
    if value.startswith("-"):
        value = value[1:].strip()
    return value


def _append_value(sections: DefaultDict[str, list[str]], field: str, value: str) -> None:
    cleaned = _clean_value(value)
    if cleaned:
        sections[field].append(cleaned)


def _split_labeled_line(line: str) -> tuple[str | None, str | None]:
    if ":" not in line:
        return None, None
    label, value = line.split(":", 1)
    field = _normalise_label(label)
    if field is None:
        return None, None
    return field, value.strip()


def parse_transcript_sections(transcript: str) -> dict[str, list[str]]:
    """Parse section-labeled transcript text into raw section values.

    Supported shape:

    ```text
    Workflow: customer_refund_processing
    Action: Agent issued a refund.
    Permission boundary: Refunds above $100 need approval.
    Evidence before action:
    - Customer email requesting refund
    Missing evidence:
    - Human approval record
    Recommendation: ESCALATE
    ```
    """

    if not isinstance(transcript, str) or not transcript.strip():
        raise IntakeValidationError("transcript must be a non-empty string")

    sections: DefaultDict[str, list[str]] = defaultdict(list)
    current_field: str | None = None

    for raw_line in transcript.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        field, value = _split_labeled_line(line)
        if field is not None:
            current_field = field
            if value:
                _append_value(sections, field, value)
            continue

        if current_field in LIST_FIELDS and line.startswith("-"):
            _append_value(sections, current_field, line)
            continue

        if current_field is not None and current_field not in LIST_FIELDS:
            _append_value(sections, current_field, line)

    return dict(sections)


def _one(sections: dict[str, list[str]], field: str) -> str | None:
    values = sections.get(field) or []
    if not values:
        return None
    return " ".join(values).strip()


def _many(sections: dict[str, list[str]], field: str) -> list[str]:
    return list(sections.get(field) or [])


def _validate_required_extracted(sections: dict[str, list[str]]) -> None:
    missing = [field for field in sorted(REQUIRED_EXTRACTED_FIELDS) if not _one(sections, field)]
    if missing:
        raise IntakeValidationError(
            "transcript missing required section(s): " + ", ".join(missing)
        )


def extract_intake_from_transcript(
    transcript: str,
    *,
    incident_id: str,
    agent_name: str,
    reporter: str | None = None,
    occurred_at: str | None = None,
) -> IntakeRecord:
    """Create a draft IntakeRecord from a lightly structured transcript.

    The transcript must provide Workflow, Action, and Permission boundary.
    The caller supplies stable metadata like incident_id and agent_name.
    """

    sections = parse_transcript_sections(transcript)
    _validate_required_extracted(sections)

    payload = {
        "incident_id": incident_id,
        "agent_name": agent_name,
        "workflow": _one(sections, "workflow"),
        "action": _one(sections, "action"),
        "permission_boundary": _one(sections, "permission_boundary"),
        "transcript": transcript,
        "reporter": reporter,
        "occurred_at": occurred_at,
        "evidence_before_action": _many(sections, "evidence_before_action"),
        "missing_evidence": _many(sections, "missing_evidence"),
        "reversibility_risks": _many(sections, "reversibility_risks"),
        "recommendation": _one(sections, "recommendation"),
        "notes": _one(sections, "notes"),
    }

    return IntakeRecord.from_dict(payload)
