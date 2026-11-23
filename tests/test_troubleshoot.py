from __future__ import annotations

import sys

import pytest

from jupyter_core import troubleshoot


@pytest.mark.parametrize("pip_output", [None, "example-package 1.0"])
def test_troubleshoot(capsys, monkeypatch, pip_output):
    """Report runtime diagnostics even when pip is unavailable."""

    def command_output(command):
        if command == [sys.executable, "-m", "pip", "list"]:
            return pip_output
        return None

    monkeypatch.setattr(troubleshoot, "subs", command_output)
    troubleshoot.main()
    out = capsys.readouterr().out
    assert "sys.executable:" in out
    assert sys.executable in out
    assert ("pip list:" in out) == (pip_output is not None)
    if pip_output is not None:
        assert pip_output in out
