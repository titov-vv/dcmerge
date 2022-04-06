import os
import sys
import filecmp
from dcmerge import main


def test_dcmerge(monkeypatch, tmp_path):
    output = str(tmp_path) + os.sep + "output.dc1"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['dcmerge', '--base', './ilya2021.dc1', '--add', './my.dc1', '--out', output])
        assert main() is None
        assert filecmp.cmp('./result.dc1', output)
        os.remove(output)
