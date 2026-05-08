# voice-to-evidence

> Most teams cannot audit what they cannot even describe.
> Voice intake turns messy agent incidents into structured safety evidence.

**Core question this project takes seriously:**

> Your AI agent may produce the right output.
> But can you prove it was *allowed* to do what it did?

`voice-to-evidence` is an experimental **voice / transcript intake layer for
AI-agent safety review**. A human (operator, reviewer, on-call engineer)
describes what an AI agent did. The system turns that messy description into a
**structured evidence artifact** and a draft **Agent Action Audit Snapshot**
that a human reviewer can act on.

This repository is the deterministic core of that idea. Voice transcription
and richer extraction are intentionally out of scope for the MVP.

---

## What this is

A small Python package + CLI that:

1. Takes a structured JSON intake describing one AI-agent action.
2. Validates the required fields.
3. Renders a Markdown **Agent Action Audit Snapshot** draft for human review.
4. Optionally extracts a draft intake from a lightly structured transcript.

The MVP flow it captures:

```
voice / transcript
  -> workflow extraction
  -> action classification
  -> permission boundary
  -> evidence before action
  -> missing evidence
  -> reversibility risks
  -> ALLOW / BLOCK / ESCALATE recommendation
  -> Agent Action Audit Snapshot draft
```

In this MVP, raw voice transcription is still outside the core. The deterministic path is:

```
lightly structured transcript -> intake draft -> validated IntakeRecord -> Snapshot draft
```

No external API calls are required.

## Why this matters

AI agents increasingly take actions, not just produce text: they refund
customers, file tickets, edit configuration, send emails. When something goes
wrong, the postmortem is usually a Slack thread and a half-remembered story.

Safety review needs a stable artifact:

- *what* the agent did,
- *what permission* it was operating under,
- *what evidence* it had before acting,
- *what evidence is missing*,
- *what is hard to reverse*,
- and a draft recommendation for a human reviewer.

`voice-to-evidence` is the intake shape for that artifact.

## MVP flow

```
intake.json  ──►  IntakeRecord  ──►  render_snapshot()  ──►  Snapshot.md
                  (validated)                              (human review)
```

Transcript draft flow:

```
transcript.txt -> extract_intake_from_transcript() -> IntakeRecord -> Snapshot.md
```

## Example

Input — `examples/intake_example.json` (excerpt):

```json
{
  "incident_id": "VTE-2026-0001",
  "agent_name": "support-triage-agent",
  "workflow": "customer_refund_processing",
  "action": "Agent issued a $480 refund ... without prior human approval.",
  "permission_boundary": "Agent is permitted to draft refunds up to $100 ...",
  "missing_evidence": ["Approval record from human reviewer", "..."],
  "reversibility_risks": ["Refund already settled to the card ..."],
  "recommendation": "ESCALATE"
}
```

Output (excerpt):

```markdown
# Agent Action Audit Snapshot — VTE-2026-0001

## Action
Agent issued a $480 refund to the customer's card on file directly, without
prior human approval.

## Permission boundary
Agent is permitted to draft and recommend refunds up to $100; refunds above
that require human approval in the support console.

## Missing evidence
- Order history lookup confirming purchase amount
- Approval record from human reviewer
- Fraud-signal check for the customer account

## Review
**Recommendation (draft):** `ESCALATE`
```

Transcript example — `examples/transcript_example.txt`:

```text
Workflow: customer_refund_processing
Action: Agent issued a $480 refund without prior human approval.
Permission boundary: Refunds above $100 require human approval.
Missing evidence:
- Approval record from human reviewer
Recommendation: ESCALATE
```

A complete example lives in [`docs/SAMPLE_SESSION.md`](docs/SAMPLE_SESSION.md),
[`docs/SNAPSHOT_OUTPUT.md`](docs/SNAPSHOT_OUTPUT.md), and
[`docs/TRANSCRIPT_EXTRACTION.md`](docs/TRANSCRIPT_EXTRACTION.md).

## Relationship to Agent Action Audit Snapshot

The **Agent Action Audit Snapshot** is the artifact this project produces — a
short, structured, human-readable record of *one* agent action and the
evidence around it. `voice-to-evidence` is an *intake layer* that produces
*draft* Snapshots. A human reviewer is always expected to validate, edit, or
override.

## Quickstart

Requires Python 3.9+. No third-party runtime dependencies.

```bash
git clone https://github.com/safal207/voice-to-evidence.git
cd voice-to-evidence

# Run the CLI on the bundled JSON example
python -m voice_to_evidence examples/intake_example.json

# Or write the Snapshot to a file
python -m voice_to_evidence examples/intake_example.json \
  --output examples/generated_snapshot.md
```

Run the transcript CLI:

```bash
python -m voice_to_evidence transcript examples/transcript_example.txt \
  --incident-id VTE-2026-0002 \
  --agent-name support-triage-agent
```

Or write the transcript-derived Snapshot to a file:

```bash
python -m voice_to_evidence transcript examples/transcript_example.txt \
  --incident-id VTE-2026-0002 \
  --agent-name support-triage-agent \
  --output examples/generated_transcript_snapshot.md
```

Use the transcript extractor from Python:

```python
from pathlib import Path
from voice_to_evidence import extract_intake_from_transcript, render_snapshot

transcript = Path("examples/transcript_example.txt").read_text()
record = extract_intake_from_transcript(
    transcript,
    incident_id="VTE-2026-0002",
    agent_name="support-triage-agent",
)
print(render_snapshot(record))
```

Run the tests:

```bash
pip install -e ".[dev]"
pytest
```

Or via the Makefile:

```bash
make test
make snapshot
make transcript-snapshot
```

## Non-goals

This project does **not** try to:

- transcribe live voice or run ASR (out of scope for MVP),
- call any external LLM or API,
- automatically remediate or roll back agent actions,
- score agents or rank vendors,
- replace existing audit logs, SIEMs, or incident management tools.

## Safety boundaries

**This project does not provide:**

- legal advice
- compliance certification
- production sign-off
- penetration testing
- autonomous remediation
- a full AI safety guarantee

**It provides:**

- structured evidence intake for one AI-agent workflow
- a draft review artifact for human evaluation

The Snapshot output is a *draft* for a human reviewer. Treat it as input to
your safety process, not a verdict.

## Project layout

```
voice-to-evidence/
├── src/voice_to_evidence/   # package: intake, extractor, snapshot, CLI
├── tests/                   # pytest suite
├── examples/                # sample intake JSON and transcript
└── docs/                    # concept, architecture, schema, samples
```

## Documentation

- [`docs/GRANT_CONCEPT.md`](docs/GRANT_CONCEPT.md) — what this is, framed for
  research / grant readers.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — how the pieces fit.
- [`docs/INTAKE_SCHEMA.md`](docs/INTAKE_SCHEMA.md) — JSON intake schema.
- [`docs/SAMPLE_SESSION.md`](docs/SAMPLE_SESSION.md) — voice → JSON → Snapshot.
- [`docs/SNAPSHOT_OUTPUT.md`](docs/SNAPSHOT_OUTPUT.md) — output format.
- [`docs/TRANSCRIPT_EXTRACTION.md`](docs/TRANSCRIPT_EXTRACTION.md) — deterministic transcript-to-intake draft extraction.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). This is an early scaffold; small,
focused PRs and concrete intake examples from real agent workflows are very
welcome.

## License

MIT — see [`LICENSE`](LICENSE).
