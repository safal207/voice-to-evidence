from voice_to_evidence.protocol import (
    INTAKE_QUESTIONS,
    iter_required_questions,
    render_intake_protocol,
)


def test_protocol_has_ten_questions():
    assert len(INTAKE_QUESTIONS) == 10
    assert INTAKE_QUESTIONS[0].id == "Q1"
    assert INTAKE_QUESTIONS[-1].id == "Q10"


def test_required_questions_map_to_core_intake_fields():
    required = iter_required_questions()
    assert {q.maps_to for q in required} == {
        "action",
        "workflow",
        "permission_boundary",
    }


def test_render_intake_protocol_contains_questions_and_metadata():
    markdown = render_intake_protocol()

    assert "Voice-to-Evidence Intake Question Protocol" in markdown
    assert "What did the AI agent do or propose?" in markdown
    assert "Maps to" in markdown
    assert "permission_boundary" in markdown


def test_render_intake_protocol_can_hide_metadata():
    markdown = render_intake_protocol(include_metadata=False)

    assert "What did the AI agent do or propose?" in markdown
    assert "Maps to" not in markdown
