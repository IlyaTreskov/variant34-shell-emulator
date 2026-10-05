import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from emulator.shell import Shell
from emulator.vfs import VirtualFileSystem


class Stage1ShellTests(unittest.TestCase):
    def test_unknown_command(self):
        shell = Shell(VirtualFileSystem())
        ok, output = shell.execute("something")
        self.assertFalse(ok)
        self.assertEqual(output, "unknown command: something")

    def test_exit(self):
        shell = Shell(VirtualFileSystem())
        ok, _ = shell.execute("exit")
        self.assertTrue(ok)
        self.assertTrue(shell.should_exit)


if __name__ == "__main__":
    unittest.main()
