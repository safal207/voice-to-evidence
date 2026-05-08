"""Command-line entry point for voice-to-evidence."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from voice_to_evidence.intake import IntakeValidationError, load_intake_from_file
from voice_to_evidence.snapshot import render_snapshot


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="voice-to-evidence",
        description=(
            "Convert a structured intake JSON describing one AI-agent action "
            "into a Markdown Agent Action Audit Snapshot draft."
        ),
    )
    parser.add_argument("intake", help="Path to intake JSON file")
    parser.add_argument(
        "--output",
        "-o",
        help="Write Snapshot Markdown to this path instead of stdout",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        record = load_intake_from_file(args.intake)
    except IntakeValidationError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    snapshot = render_snapshot(record)

    if args.output:
        Path(args.output).write_text(snapshot, encoding="utf-8")
        print(f"wrote snapshot to {args.output}")
    else:
        sys.stdout.write(snapshot)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
