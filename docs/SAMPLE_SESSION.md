# Sample session

This walks through how a real intake might flow from a voice note to a
Snapshot draft. Everything to the left of `intake.json` is *outside* this MVP
— shown here only for context.

## 1. Voice note (raw)

> "So the agent got a refund request from a customer, and instead of just
> flagging it for review like usual, it actually went ahead and issued a $480
> refund directly to the card on file. I'm not sure it had permission to do
> that. We saw the email afterwards, the agent didn't check the order history
> first either."

## 2. Structured intake (`intake.json`)

The reporter — or upstream tooling — turns that into a structured intake
matching [`INTAKE_SCHEMA.md`](INTAKE_SCHEMA.md). See
[`examples/intake_example.json`](../examples/intake_example.json) for the full
file.

## 3. Run the CLI

```bash
python -m voice_to_evidence examples/intake_example.json \
  --output examples/generated_snapshot.md
```

## 4. Review the Snapshot

The generated Markdown lands in `examples/generated_snapshot.md` and looks
like the example in [`SNAPSHOT_OUTPUT.md`](SNAPSHOT_OUTPUT.md). It is a
*draft* — a human reviewer is expected to confirm, edit, or override the
recommendation before any decision is acted on.

## 5. Hand off

Typical next steps (out of scope for this repo):

- attach the Snapshot to the incident ticket,
- file a permission-boundary review for the agent,
- update the agent's tool / approval policy if needed.
