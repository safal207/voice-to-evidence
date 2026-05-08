# Intake schema

The intake is a single JSON object describing **one** AI-agent action.

## Required fields

| Field                  | Type   | Description |
|------------------------|--------|-------------|
| `incident_id`          | string | Stable identifier for this incident, e.g. `VTE-2026-0001`. |
| `agent_name`           | string | Name/identifier of the AI agent that took the action. |
| `workflow`             | string | The workflow the agent was operating in (e.g. `customer_refund_processing`). |
| `action`               | string | What the agent actually did, in plain language. |
| `permission_boundary`  | string | The policy / boundary the agent was operating under. |

## Optional fields

| Field                     | Type            | Description |
|---------------------------|-----------------|-------------|
| `transcript`              | string          | Original human description (e.g. transcribed voice note). |
| `reporter`                | string          | Who filed the intake. |
| `occurred_at`             | string          | ISO 8601 timestamp of the action. |
| `evidence_before_action`  | list of strings | Evidence available to the agent *before* it acted. |
| `missing_evidence`        | list of strings | Evidence the reviewer believes was *required but missing*. |
| `reversibility_risks`     | list of strings | Reasons this action is hard or expensive to undo. |
| `recommendation`          | string          | One of `ALLOW`, `BLOCK`, `ESCALATE` (case-insensitive). |
| `notes`                   | string          | Free-form reviewer notes. |

## Validation rules

- All required fields must be non-empty strings.
- List fields, if present, must be lists of strings.
- `recommendation`, if present, must be one of `ALLOW`, `BLOCK`, `ESCALATE`
  and is normalised to upper case.
- Validation errors raise `IntakeValidationError`.

## Minimal example

```json
{
  "incident_id": "VTE-1",
  "agent_name": "agent",
  "workflow": "wf",
  "action": "did something",
  "permission_boundary": "limited"
}
```

## Full example

See [`examples/intake_example.json`](../examples/intake_example.json).
