# Transcript Extraction

This document describes the deterministic transcript-to-intake draft layer.

## Purpose

The first MVP accepted already-structured JSON.

This layer adds the previous step:

```text
lightly structured transcript
-> intake draft
-> Snapshot draft
-> human review
```

It is intentionally not an LLM extractor and not a voice API integration.

## Why deterministic first

Voice and LLM extraction can come later, but the safety-review core needs a stable contract first.

The transcript extractor is designed to be:

- dependency-free,
- deterministic,
- easy to test,
- explicit about missing sections,
- safe to replace later with a voice/LLM layer.

## Supported transcript shape

Use labeled sections:

```text
Workflow: customer_refund_processing
Action: Agent issued a $480 refund without human approval.
Permission boundary: Refunds above $100 require human approval.
Evidence before action:
- Customer email requesting refund
Missing evidence:
- Human approval record
Reversibility risks:
- Refund already settled to the card
Recommendation: ESCALATE
Notes: Likely permission-boundary violation.
```

Required sections:

- `Workflow`
- `Action`
- `Permission boundary`

Optional sections:

- `Evidence before action`
- `Missing evidence`
- `Reversibility risks`
- `Recommendation`
- `Notes`

## API usage

```python
from pathlib import Path
from voice_to_evidence.extractor import extract_intake_from_transcript
from voice_to_evidence.snapshot import render_snapshot

transcript = Path("examples/transcript_example.txt").read_text()
record = extract_intake_from_transcript(
    transcript,
    incident_id="VTE-2026-0002",
    agent_name="support-triage-agent",
)
print(render_snapshot(record))
```

## Boundary

This is not natural-language understanding.

If the transcript has no labels, the extractor should not guess silently. It should ask for clearer structure or hand off to a later optional LLM layer.

## Future layer

Later:

```text
raw voice
-> speech-to-text
-> LLM-assisted structured extraction
-> deterministic intake validation
-> Snapshot draft
```

The boundary remains:

```text
LLM may draft.
Deterministic validation decides whether the draft is admissible.
```
