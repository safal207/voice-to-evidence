# Grant / research concept

## One-liner

`voice-to-evidence` is a **voice intake layer for AI-agent safety review**: it
turns messy human descriptions of agent incidents into structured evidence
artifacts a human reviewer can act on.

## Problem

AI agents now take consequential actions: refunds, ticket changes,
configuration edits, outbound messages. When something goes wrong, the
post-incident record is usually a Slack thread.

Two gaps follow:

1. **Description gap.** The people closest to the incident (operators,
   support engineers, on-call) describe what happened in natural language,
   not in a structured form a safety reviewer can audit.
2. **Evidence gap.** Even when the agent's *output* is correct, teams often
   cannot show that the agent was *allowed* to do what it did, or that the
   evidence required by policy was actually present before the action.

## Hypothesis

If incident intake is captured against a small, fixed schema —
*workflow / action / permission boundary / evidence before / missing evidence
/ reversibility risks / recommendation* — then:

- review becomes faster and more comparable across incidents,
- gaps in agent permission design become visible across many incidents,
- the artifact (the **Agent Action Audit Snapshot**) becomes a stable input
  to existing safety / governance processes.

## Scope of this repository

A deterministic, dependency-free Python core:

- intake schema and validation,
- Markdown Snapshot rendering,
- CLI for local use and scripting,
- examples and docs.

## Out of scope (intentionally)

- live voice transcription / ASR,
- LLM-based extraction from raw transcripts,
- automated agent remediation,
- compliance certification of any kind.

## What would make this useful

- A small library of real-world intake examples across different agent
  workflows.
- Integration points (export, webhook, ticket creation) added *after* the
  core schema has stabilised.
- Calibration: do reviewers actually find Snapshots faster to act on than
  free-text incident reports?
