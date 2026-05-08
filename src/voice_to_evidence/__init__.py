"""Voice-to-Evidence: structured evidence intake for AI-agent safety review."""

from voice_to_evidence.extractor import (
    extract_intake_from_transcript,
    parse_transcript_sections,
)
from voice_to_evidence.intake import (
    IntakeRecord,
    IntakeValidationError,
    load_intake,
    load_intake_from_file,
)
from voice_to_evidence.protocol import (
    INTAKE_QUESTIONS,
    IntakeQuestion,
    iter_required_questions,
    render_intake_protocol,
)
from voice_to_evidence.snapshot import render_snapshot

__all__ = [
    "INTAKE_QUESTIONS",
    "IntakeQuestion",
    "IntakeRecord",
    "IntakeValidationError",
    "extract_intake_from_transcript",
    "iter_required_questions",
    "load_intake",
    "load_intake_from_file",
    "parse_transcript_sections",
    "render_intake_protocol",
    "render_snapshot",
]

__version__ = "0.4.0"
