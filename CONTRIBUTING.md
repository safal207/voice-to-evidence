# Contributing to voice-to-evidence

Thanks for your interest. This project is an early scaffold; the goal is a
small, deterministic, well-tested intake core that real safety-review
workflows can build on.

## Ground rules

- Keep the runtime dependency-free where possible. The MVP is intentionally
  Python stdlib only.
- Do not add OpenAI / LLM / cloud-API dependencies to the core package without
  discussion. Voice/LLM extraction belongs in a separate optional layer.
- Do not claim production-readiness, compliance certification, or autonomous
  safety guarantees in code, docs, or commit messages.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## What good PRs look like

- A clear motivating example (ideally a real agent workflow).
- A test for new behaviour.
- Docs updated when the schema or output format changes.
- No new heavy dependencies in the core.

## Reporting issues

Please include:

- a minimal intake JSON that reproduces the problem,
- expected vs. actual Snapshot output,
- Python version and OS.

## Scope

In scope:
- intake schema, validation, Snapshot rendering, CLI ergonomics, docs.

Out of scope (for now):
- live ASR / voice transcription,
- LLM-based extraction,
- automated remediation of agent actions.
