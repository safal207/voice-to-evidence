import json
from pathlib import Path

import pytest

from voice_to_evidence.intake import (
    IntakeRecord,
    IntakeValidationError,
    load_intake,
    load_intake_from_file,
)

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "intake_example.json"


def _minimal_payload(**overrides):
    base = {
        "incident_id": "VTE-1",
        "agent_name": "agent",
        "workflow": "wf",
        "action": "did something",
        "permission_boundary": "limited",
    }
    base.update(overrides)
    return base


def test_loads_example_file():
    record = load_intake_from_file(EXAMPLE)
    assert isinstance(record, IntakeRecord)
    assert record.incident_id == "VTE-2026-0001"
    assert record.recommendation == "ESCALATE"
    assert "Order history lookup" in record.missing_evidence[0]


def test_load_intake_from_string():
    payload = json.dumps(_minimal_payload())
    record = load_intake(payload)
    assert record.agent_name == "agent"
    assert record.evidence_before_action == []


def test_missing_required_fields():
    with pytest.raises(IntakeValidationError) as excinfo:
        IntakeRecord.from_dict({"incident_id": "x"})
    assert "missing required field" in str(excinfo.value)


def test_invalid_json_raises():
    with pytest.raises(IntakeValidationError):
        load_intake("{not json")


def test_recommendation_must_be_known():
    with pytest.raises(IntakeValidationError):
        IntakeRecord.from_dict(_minimal_payload(recommendation="MAYBE"))


def test_recommendation_normalized_uppercase():
    record = IntakeRecord.from_dict(_minimal_payload(recommendation="allow"))
    assert record.recommendation == "ALLOW"


def test_list_field_must_be_strings():
    with pytest.raises(IntakeValidationError):
        IntakeRecord.from_dict(_minimal_payload(evidence_before_action=[1, 2]))


def test_missing_file_raises():
    with pytest.raises(IntakeValidationError):
        load_intake_from_file("/nonexistent/intake.json")
