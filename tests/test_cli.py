from pathlib import Path

import pytest

from voice_to_evidence.cli import main

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "intake_example.json"


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
    assert "wrote snapshot" in msg


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
