"""Smoke tests for the unitconv CLI entrypoint."""

import pytest

from unitconv.cli import main


def test_help_exits_cleanly(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "usage" in captured.out.lower()
