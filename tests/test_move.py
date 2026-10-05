import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from emulator.shell import Shell
from emulator.vfs import VirtualFileSystem


class MoveTests(unittest.TestCase):
    def test_rename(self):
        vfs = VirtualFileSystem()
        path = os.path.join(os.path.dirname(__file__), "..", "examples", "vfs", "demo.xml")
        vfs.load(path)
        shell = Shell(vfs)
        ok, _ = shell.execute("mv /readme.txt /about.txt")
        self.assertTrue(ok)
        ok, output = shell.execute("ls /")
        self.assertTrue(ok)
        self.assertIn("about.txt", output)
        self.assertNotIn("readme.txt", output)


if __name__ == "__main__":
    unittest.main()
