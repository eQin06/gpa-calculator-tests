"""End-to-end tests for R8: run the program as a separate process."""
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "gpa_calculator", *args],
        capture_output=True, text=True, cwd=PROJECT_ROOT,
    )


def test_cli_prints_gpa_and_standing():
    result = run_cli("CMPE411:87:6", "MATH101:72:4")
    assert result.returncode == 0
    assert result.stdout.splitlines() == ["GPA: 2.90", "Standing: Satisfactory"]


def test_cli_high_honor():
    result = run_cli("A:95:8", "B:92:8")
    assert result.returncode == 0
    assert "Standing: High Honor" in result.stdout


def test_cli_without_arguments_fails():
    result = run_cli()
    assert result.returncode == 2
    assert result.stderr.startswith("Error:")


def test_cli_rejects_out_of_range_score():
    result = run_cli("A:101:3")
    assert result.returncode == 2
    assert result.stderr.startswith("Error:")


def test_cli_rejects_malformed_argument():
    result = run_cli("CMPE411-87-6")
    assert result.returncode == 2
    assert result.stderr.startswith("Error:")