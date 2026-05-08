# Architecture

`voice-to-evidence` is intentionally small. The MVP is one process, no
network, no third-party runtime dependencies.

## Components

```
┌────────────────────┐    ┌────────────────────┐    ┌────────────────────┐
│  intake JSON file  │ -> │  IntakeRecord      │ -> │  Snapshot Markdown │
│  (human-curated)   │    │  (validated)       │    │  (draft artifact)  │
└────────────────────┘    └────────────────────┘    └────────────────────┘
                              ▲                          ▲
                              │                          │
                       intake.py                    snapshot.py
                              ▲                          ▲
                              └──────── cli.py ──────────┘
```

### `intake.py`
- Defines `IntakeRecord` (a dataclass).
- Defines `REQUIRED_FIELDS` and `ALLOWED_RECOMMENDATIONS`.
- Provides `load_intake(str)` and `load_intake_from_file(path)`.
- All validation errors raise `IntakeValidationError`.

### `snapshot.py`
- Pure function `render_snapshot(record) -> str` that produces a Markdown
  Agent Action Audit Snapshot draft.
- No I/O, no randomness — given the same record, the output is the same.

### `cli.py` / `__main__.py`
- `python -m voice_to_evidence <intake.json>`
- `--output PATH` to write the Snapshot to a file instead of stdout.
- Returns exit code `2` on validation errors.

## Where voice fits (later)

```
[microphone] -> [ASR] -> [structured-extraction] -> intake.json -> THIS REPO
```

Everything left of `intake.json` is intentionally *outside* this MVP. The
contract that makes the rest of the pipeline replaceable is the **intake
schema** in [`INTAKE_SCHEMA.md`](INTAKE_SCHEMA.md).

## Design choices

- **Deterministic core.** No LLM in the validation/render path. Reviewers
  need to trust that the same intake produces the same Snapshot.
- **One incident per record.** Aggregation across incidents is a separate
  concern.
- **Markdown output.** Easy to paste into tickets, PRs, postmortems; easy to
  diff in version control.
- **Dataclass + JSON, not Pydantic.** Keeps the dependency surface minimal
  for the MVP. Can be swapped later without changing the public API.
