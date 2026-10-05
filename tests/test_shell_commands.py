import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from emulator.shell import Shell
from emulator.vfs import VirtualFileSystem


def make_shell():
    vfs = VirtualFileSystem()
    path = os.path.join(os.path.dirname(__file__), "..", "examples", "vfs", "demo.xml")
    vfs.load(path)
    return Shell(vfs)


class ShellCommandTests(unittest.TestCase):
    def test_ls(self):
        shell = make_shell()
        ok, output = shell.execute("ls /")
        self.assertTrue(ok)
        self.assertIn("home/", output)

    def test_cd(self):
        shell = make_shell()
        ok, _ = shell.execute("cd /home/student")
        self.assertTrue(ok)
        self.assertEqual(shell.cwd, "/home/student")

    def test_head(self):
        shell = make_shell()
        ok, output = shell.execute("head -n 2 /home/student/notes.txt")
        self.assertTrue(ok)
        self.assertEqual(output, "first line\nsecond line")

    def test_tac(self):
        shell = make_shell()
        ok, output = shell.execute("tac /home/student/notes.txt")
        self.assertTrue(ok)
        self.assertTrue(output.startswith("fifth line"))

    def test_history(self):
        shell = make_shell()
        shell.execute("ls /")
        ok, output = shell.execute("history")
        self.assertTrue(ok)
        self.assertIn("1  ls /", output)


if __name__ == "__main__":
    unittest.main()
