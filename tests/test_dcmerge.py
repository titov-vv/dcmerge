import sys
from dcmerge import main


def test_dcmerge(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['dcmerge', '--base', './base.dc1', '--add', './delta.dc1'])
        assert main() is None
