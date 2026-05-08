import pytest

from voice_to_evidence.extractor import (
    extract_intake_from_transcript,
    parse_transcript_sections,
)
from voice_to_evidence.intake import IntakeValidationError

TRANSCRIPT = """Workflow: customer_refund_processing
Action: Agent issued a $480 refund without prior human approval.
Permission boundary: Refunds above $100 require human approval.
Evidence before action:
- Customer email requesting refund
- Order ID referenced in customer message
Missing evidence:
- Approval record from human reviewer
Reversibility risks:
- Refund already settled to the card
Recommendation: escalate
Notes: Needs human review.
"""


def test_parse_transcript_sections_extracts_lists():
    sections = parse_transcript_sections(TRANSCRIPT)

    assert sections["workflow"] == ["customer_refund_processing"]
    assert sections["evidence_before_action"] == [
        "Customer email requesting refund",
        "Order ID referenced in customer message",
    ]
    assert sections["missing_evidence"] == ["Approval record from human reviewer"]


def test_extract_intake_from_transcript_builds_record():
    record = extract_intake_from_transcript(
        TRANSCRIPT,
        incident_id="VTE-2",
        agent_name="support-triage-agent",
        reporter="ops",
    )

    assert record.incident_id == "VTE-2"
    assert record.workflow == "customer_refund_processing"
    assert record.agent_name == "support-triage-agent"
    assert record.reporter == "ops"
    assert record.recommendation == "ESCALATE"
    assert record.missing_evidence == ["Approval record from human reviewer"]


def test_extract_intake_requires_labeled_core_sections():
    with pytest.raises(IntakeValidationError) as excinfo:
        extract_intake_from_transcript(
            "Action: Agent did something.",
            incident_id="VTE-3",
            agent_name="agent",
        )

    assert "transcript missing required section" in str(excinfo.value)


def test_parse_transcript_rejects_empty_transcript():
    with pytest.raises(IntakeValidationError):
        parse_transcript_sections("   ")
