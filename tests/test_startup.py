import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from emulator.shell import Shell
from emulator.startup import run_startup_script
from emulator.vfs import VirtualFileSystem


class StartupTests(unittest.TestCase):
    def test_stops_on_error(self):
        shell = Shell(VirtualFileSystem())
        output = []
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".txt") as handle:
            handle.write("ls /\nunknown\nls /\n")
            path = handle.name
        try:
            result = run_startup_script(path, shell, output.append)
        finally:
            os.unlink(path)
        self.assertFalse(result)
        self.assertTrue(any("startup stopped" in line for line in output))
        self.assertEqual(shell.history_items, ["ls /", "unknown"])


if __name__ == "__main__":
    unittest.main()
