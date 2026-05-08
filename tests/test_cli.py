from pathlib import Path

import pytest

from voice_to_evidence.cli import main

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "intake_example.json"
TRANSCRIPT = Path(__file__).resolve().parents[1] / "examples" / "transcript_example.txt"


def test_cli_writes_to_stdout(capsys):
    rc = main([str(EXAMPLE)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Agent Action Audit Snapshot" in out
    assert "VTE-2026-0001" in out


def test_cli_output_flag(tmp_path, capsys):
    out_path = tmp_path / "snapshot.md"
    rc = main([str(EXAMPLE), "--output", str(out_path)])
    assert rc == 0
    assert out_path.exists()
    text = out_path.read_text(encoding="utf-8")
    assert "VTE-2026-0001" in text
    msg = capsys.readouterr().out
    assert "wrote" in msg


def test_cli_protocol_writes_to_stdout(capsys):
    rc = main(["protocol"])
    out = capsys.readouterr().out

    assert rc == 0
    assert "Voice-to-Evidence Intake Question Protocol" in out
    assert "What did the AI agent do or propose?" in out
    assert "Maps to" in out


def test_cli_protocol_no_metadata(capsys):
    rc = main(["protocol", "--no-metadata"])
    out = capsys.readouterr().out

    assert rc == 0
    assert "What did the AI agent do or propose?" in out
    assert "Maps to" not in out


def test_cli_protocol_output_flag(tmp_path, capsys):
    out_path = tmp_path / "protocol.md"
    rc = main(["protocol", "--output", str(out_path)])

    assert rc == 0
    assert out_path.exists()
    assert "Voice-to-Evidence Intake Question Protocol" in out_path.read_text(encoding="utf-8")
    assert "wrote" in capsys.readouterr().out


def test_cli_transcript_writes_to_stdout(capsys):
    rc = main([
        "transcript",
        str(TRANSCRIPT),
        "--incident-id",
        "VTE-2026-0002",
        "--agent-name",
        "support-triage-agent",
    ])
    out = capsys.readouterr().out

    assert rc == 0
    assert "Agent Action Audit Snapshot" in out
    assert "VTE-2026-0002" in out
    assert "support-triage-agent" in out
    assert "ESCALATE" in out


def test_cli_transcript_output_flag(tmp_path, capsys):
    out_path = tmp_path / "transcript_snapshot.md"
    rc = main([
        "transcript",
        str(TRANSCRIPT),
        "--incident-id",
        "VTE-2026-0003",
        "--agent-name",
        "support-triage-agent",
        "--output",
        str(out_path),
    ])

    assert rc == 0
    assert out_path.exists()
    text = out_path.read_text(encoding="utf-8")
    assert "VTE-2026-0003" in text
    assert "customer_refund_processing" in text
    assert "wrote" in capsys.readouterr().out


def test_cli_transcript_missing_file_returns_error(capsys):
    rc = main([
        "transcript",
        "/no/such/transcript.txt",
        "--incident-id",
        "VTE-404",
        "--agent-name",
        "agent",
    ])

    assert rc == 2
    assert "transcript file not found" in capsys.readouterr().err


def test_cli_missing_file_returns_error(capsys):
    rc = main(["/no/such/file.json"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "error" in err


def test_cli_invalid_intake_returns_error(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text('{"incident_id": "x"}', encoding="utf-8")
    rc = main([str(bad)])
    assert rc == 2
    assert "missing required field" in capsys.readouterr().err
