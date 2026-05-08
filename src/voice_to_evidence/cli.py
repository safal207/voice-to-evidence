"""Command-line entry point for voice-to-evidence."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from voice_to_evidence.extractor import extract_intake_from_transcript
from voice_to_evidence.intake import IntakeValidationError, load_intake_from_file
from voice_to_evidence.snapshot import render_snapshot

TRANSCRIPT_COMMAND = "transcript"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="voice-to-evidence",
        description=(
            "Convert structured intake JSON or a lightly structured transcript "
            "into a Markdown Agent Action Audit Snapshot draft."
        ),
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help=(
            "Either an intake JSON path, or: transcript <transcript.txt>. "
            "The JSON path form is kept for backwards compatibility."
        ),
    )
    parser.add_argument(
        "--incident-id",
        help="Stable incident identifier required for transcript mode",
    )
    parser.add_argument(
        "--agent-name",
        help="AI-agent name required for transcript mode",
    )
    parser.add_argument("--reporter", help="Optional reporter name for transcript mode")
    parser.add_argument("--occurred-at", help="Optional occurrence timestamp for transcript mode")
    parser.add_argument(
        "--output",
        "-o",
        help="Write Snapshot Markdown to this path instead of stdout",
    )
    return parser


def _write_snapshot(snapshot: str, output: str | None) -> None:
    if output:
        Path(output).write_text(snapshot, encoding="utf-8")
        print(f"wrote snapshot to {output}")
    else:
        sys.stdout.write(snapshot)


def _render_json_intake(intake_path: str, output: str | None) -> int:
    try:
        record = load_intake_from_file(intake_path)
    except IntakeValidationError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    _write_snapshot(render_snapshot(record), output)
    return 0


def _render_transcript(
    transcript_file: str,
    *,
    incident_id: str | None,
    agent_name: str | None,
    reporter: str | None,
    occurred_at: str | None,
    output: str | None,
) -> int:
    if not incident_id:
        print("error: --incident-id is required in transcript mode", file=sys.stderr)
        return 2
    if not agent_name:
        print("error: --agent-name is required in transcript mode", file=sys.stderr)
        return 2

    transcript_path = Path(transcript_file)
    if not transcript_path.exists():
        print(f"error: transcript file not found: {transcript_path}", file=sys.stderr)
        return 2

    try:
        record = extract_intake_from_transcript(
            transcript_path.read_text(encoding="utf-8"),
            incident_id=incident_id,
            agent_name=agent_name,
            reporter=reporter,
            occurred_at=occurred_at,
        )
    except IntakeValidationError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    _write_snapshot(render_snapshot(record), output)
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.inputs[0] == TRANSCRIPT_COMMAND:
        if len(args.inputs) != 2:
            print("error: transcript mode requires exactly one transcript file", file=sys.stderr)
            return 2
        return _render_transcript(
            args.inputs[1],
            incident_id=args.incident_id,
            agent_name=args.agent_name,
            reporter=args.reporter,
            occurred_at=args.occurred_at,
            output=args.output,
        )

    if len(args.inputs) != 1:
        print("error: JSON mode requires exactly one intake file", file=sys.stderr)
        return 2

    return _render_json_intake(args.inputs[0], args.output)


if __name__ == "__main__":
    raise SystemExit(main())
