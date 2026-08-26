"""Smoke and integration tests for the unitconv CLI entrypoint."""

import subprocess
import sys

import pytest

from unitconv.cli import main


def test_help_exits_cleanly(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "usage" in captured.out.lower()


# --- direct main() invocation tests -----------------------------------


def test_temperature_subcommand_success(capsys):
    exit_code = main(["temperature", "100", "C", "F"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "212.0"


def test_length_subcommand_success(capsys):
    exit_code = main(["length", "1", "mi", "ft"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert float(captured.out.strip()) == pytest.approx(5280.0, rel=1e-6)


def test_weight_subcommand_success(capsys):
    exit_code = main(["weight", "10", "kg", "lb"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert float(captured.out.strip()) == pytest.approx(22.0462262, rel=1e-6)


def test_length_subcommand_unsupported_unit_is_clean_error(capsys):
    exit_code = main(["length", "5", "mi", "km"])
    captured = capsys.readouterr()

    assert exit_code != 0
    assert captured.out == ""
    assert "traceback" not in captured.err.lower()
    assert "Error:" in captured.err


def test_temperature_subcommand_invalid_unit_is_clean_error(capsys):
    exit_code = main(["temperature", "0", "C", "bogus"])
    captured = capsys.readouterr()

    assert exit_code != 0
    assert captured.out == ""
    assert "traceback" not in captured.err.lower()
    assert "Error:" in captured.err


def test_weight_subcommand_invalid_value_is_clean_error(capsys):
    exit_code = main(["weight", "-1", "kg", "lb"])
    captured = capsys.readouterr()

    assert exit_code != 0
    assert captured.out == ""
    assert "traceback" not in captured.err.lower()
    assert "Error:" in captured.err


# --- subprocess-level tests (exercise the real `python -m unitconv` path) --


def _run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "unitconv", *args],
        capture_output=True,
        text=True,
    )


def test_subprocess_temperature_success():
    result = _run_cli("temperature", "0", "C", "F")
    assert result.returncode == 0
    assert result.stdout.strip() == "32.0"
    assert result.stderr == ""


def test_subprocess_length_success():
    result = _run_cli("length", "5", "mi", "ft")
    assert result.returncode == 0
    assert float(result.stdout.strip()) == pytest.approx(26400.0, rel=1e-6)


def test_subprocess_weight_success():
    result = _run_cli("weight", "1", "kg", "oz")
    assert result.returncode == 0
    assert float(result.stdout.strip()) == pytest.approx(35.27396195, rel=1e-6)


def test_subprocess_length_unsupported_unit_no_traceback():
    result = _run_cli("length", "5", "mi", "km")
    assert result.returncode != 0
    assert result.stdout == ""
    assert "traceback" not in result.stderr.lower()
    assert "Error:" in result.stderr
