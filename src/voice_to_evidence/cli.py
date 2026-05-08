"""Command-line entry point for voice-to-evidence."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from voice_to_evidence.extractor import extract_intake_from_transcript
from voice_to_evidence.intake import IntakeValidationError, load_intake_from_file
from voice_to_evidence.snapshot import render_snapshot


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="voice-to-evidence",
        description=(
            "Convert structured intake JSON or a lightly structured transcript "
            "into a Markdown Agent Action Audit Snapshot draft."
        ),
    )
    subparsers = parser.add_subparsers(dest="command")

    transcript_parser = subparsers.add_parser(
        "transcript",
        help="Render a Snapshot from a lightly structured transcript file",
    )
    transcript_parser.add_argument("transcript", help="Path to transcript text file")
    transcript_parser.add_argument(
        "--incident-id",
        required=True,
        help="Stable incident identifier to attach to the extracted intake",
    )
    transcript_parser.add_argument(
        "--agent-name",
        required=True,
        help="Name or identifier of the AI agent being reviewed",
    )
    transcript_parser.add_argument("--reporter", help="Optional reporter name")
    transcript_parser.add_argument("--occurred-at", help="Optional occurrence timestamp")
    transcript_parser.add_argument(
        "--output",
        "-o",
        help="Write Snapshot Markdown to this path instead of stdout",
    )

    parser.add_argument(
        "intake",
        nargs="?",
        help="Path to intake JSON file. Kept for backwards compatibility.",
    )
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


def _render_transcript(args: argparse.Namespace) -> int:
    transcript_path = Path(args.transcript)
    if not transcript_path.exists():
        print(f"error: transcript file not found: {transcript_path}", file=sys.stderr)
        return 2

    try:
        record = extract_intake_from_transcript(
            transcript_path.read_text(encoding="utf-8"),
            incident_id=args.incident_id,
            agent_name=args.agent_name,
            reporter=args.reporter,
            occurred_at=args.occurred_at,
        )
    except IntakeValidationError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    _write_snapshot(render_snapshot(record), args.output)
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "transcript":
        return _render_transcript(args)

    if not args.intake:
        parser.error("intake JSON path is required unless using the 'transcript' command")

    return _render_json_intake(args.intake, args.output)


if __name__ == "__main__":
    raise SystemExit(main())
