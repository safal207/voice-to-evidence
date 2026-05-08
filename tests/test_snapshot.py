from pathlib import Path

from voice_to_evidence.intake import IntakeRecord, load_intake_from_file
from voice_to_evidence.snapshot import render_snapshot

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "intake_example.json"


def test_snapshot_contains_core_sections():
    record = load_intake_from_file(EXAMPLE)
    md = render_snapshot(record)

    assert "# Agent Action Audit Snapshot — VTE-2026-0001" in md
    assert "## Incident metadata" in md
    assert "## Action" in md
    assert "## Permission boundary" in md
    assert "## Evidence available before action" in md
    assert "## Missing evidence" in md
    assert "## Reversibility risks" in md
    assert "## Review" in md
    assert "ESCALATE" in md
    assert "support-triage-agent" in md


def test_snapshot_handles_minimal_record():
    record = IntakeRecord(
        incident_id="X1",
        agent_name="a",
        workflow="w",
        action="did x",
        permission_boundary="bounded",
    )
    md = render_snapshot(record)
    assert "X1" in md
    assert "_(none recorded)_" in md
    assert "human reviewer required" in md


def test_snapshot_includes_transcript_when_present():
    record = load_intake_from_file(EXAMPLE)
    md = render_snapshot(record)
    assert "## Original transcript" in md
    assert "$480 refund" in md
