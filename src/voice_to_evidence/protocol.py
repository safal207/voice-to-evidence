"""Canonical intake-question protocol for AI-agent safety review.

The protocol is intentionally deterministic and model-agnostic. A future voice
agent can use these questions as a guided interview, but the questions are
stable data rather than hidden prompt text.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass(frozen=True)
class IntakeQuestion:
    """One question in the safety-review intake protocol."""

    id: str
    question: str
    purpose: str
    maps_to: str
    required: bool = False


INTAKE_QUESTIONS: tuple[IntakeQuestion, ...] = (
    IntakeQuestion(
        id="Q1",
        question="What did the AI agent do or propose?",
        purpose="Capture the concrete action under review.",
        maps_to="action",
        required=True,
    ),
    IntakeQuestion(
        id="Q2",
        question="Which workflow or system was affected?",
        purpose="Identify the operational context and workflow boundary.",
        maps_to="workflow",
        required=True,
    ),
    IntakeQuestion(
        id="Q3",
        question="What was the agent allowed to do in this workflow?",
        purpose="Capture the permission boundary before judging the action.",
        maps_to="permission_boundary",
        required=True,
    ),
    IntakeQuestion(
        id="Q4",
        question="Could the agent execute the action directly, or only suggest it?",
        purpose="Distinguish recommendation authority from execution authority.",
        maps_to="agent_capability",
    ),
    IntakeQuestion(
        id="Q5",
        question="What evidence existed before the action happened?",
        purpose="List the facts available before the agent acted.",
        maps_to="evidence_before_action",
    ),
    IntakeQuestion(
        id="Q6",
        question="What evidence was missing or should have been checked first?",
        purpose="Expose missing preconditions, approvals, logs, or policy checks.",
        maps_to="missing_evidence",
    ),
    IntakeQuestion(
        id="Q7",
        question="Was there human review before or after the action?",
        purpose="Clarify whether review happened before execution, after execution, or not at all.",
        maps_to="current_approval",
    ),
    IntakeQuestion(
        id="Q8",
        question="What could go wrong if this action repeats at scale?",
        purpose="Surface risk propagation and repeated-action failure modes.",
        maps_to="notes",
    ),
    IntakeQuestion(
        id="Q9",
        question="How reversible is the action, and what would rollback require?",
        purpose="Capture reversibility, rollback cost, and downstream impact.",
        maps_to="reversibility_risks",
    ),
    IntakeQuestion(
        id="Q10",
        question="Should the next similar action be allowed, blocked, or escalated?",
        purpose="Produce a draft human-review recommendation.",
        maps_to="recommendation",
    ),
)


def iter_required_questions(
    questions: Iterable[IntakeQuestion] = INTAKE_QUESTIONS,
) -> tuple[IntakeQuestion, ...]:
    """Return the required questions from a protocol."""

    return tuple(question for question in questions if question.required)


def render_intake_protocol(
    questions: Iterable[IntakeQuestion] = INTAKE_QUESTIONS,
    *,
    include_metadata: bool = True,
) -> str:
    """Render the intake-question protocol as Markdown."""

    lines: list[str] = ["# Voice-to-Evidence Intake Question Protocol", ""]
    lines.append(
        "These questions guide a human or voice agent through one AI-agent action review."
    )
    lines.append("")

    for item in questions:
        required = "required" if item.required else "optional"
        lines.append(f"## {item.id}. {item.question}")
        if include_metadata:
            lines.append(f"- **Purpose:** {item.purpose}")
            lines.append(f"- **Maps to:** `{item.maps_to}`")
            lines.append(f"- **Status:** {required}")
        lines.append("")

    lines.append("---")
    lines.append(
        "_The protocol guides intake only. The resulting Snapshot remains a draft for human safety review._"
    )
    lines.append("")
    return "\n".join(lines)
