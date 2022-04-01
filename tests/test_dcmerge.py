import os
import sys
import filecmp
from dcmerge import main


def test_dcmerge(monkeypatch, tmp_path):
    output = str(tmp_path) + os.sep + "output.dc1"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['dcmerge', '--base', './base.dc1', '--add', './delta.dc1', '--out', output])
        assert main() is None
        assert filecmp.cmp('./base.dc1', output)
        os.remove(output)
