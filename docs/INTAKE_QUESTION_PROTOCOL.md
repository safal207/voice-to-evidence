# Intake Question Protocol

This protocol defines the canonical questions for a guided AI-agent safety-review intake.

The goal is not to make a voice agent conversationally impressive.

The goal is to make the interview structured enough that a messy incident can become a reviewable evidence artifact.

## Core flow

```text
question protocol
-> human / voice answers
-> transcript
-> intake draft
-> validated IntakeRecord
-> Snapshot draft
-> human review
```

## Questions

1. What did the AI agent do or propose?
2. Which workflow or system was affected?
3. What was the agent allowed to do in this workflow?
4. Could the agent execute the action directly, or only suggest it?
5. What evidence existed before the action happened?
6. What evidence was missing or should have been checked first?
7. Was there human review before or after the action?
8. What could go wrong if this action repeats at scale?
9. How reversible is the action, and what would rollback require?
10. Should the next similar action be allowed, blocked, or escalated?

## Required questions

The minimum required questions are:

- action
- workflow
- permission boundary

Without these, the system should not generate a confident Snapshot draft.

## CLI usage

```bash
python -m voice_to_evidence protocol
```

Without metadata:

```bash
python -m voice_to_evidence protocol --no-metadata
```

Write to file:

```bash
python -m voice_to_evidence protocol --output examples/generated_protocol.md
```

## Design rule

```text
A voice agent may ask the questions.
The deterministic protocol defines what must be asked.
The Snapshot remains a draft for human safety review.
```
