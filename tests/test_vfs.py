import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from emulator.vfs import VirtualFileSystem


class VFSTests(unittest.TestCase):
    def test_load_demo(self):
        vfs = VirtualFileSystem()
        path = os.path.join(os.path.dirname(__file__), "..", "examples", "vfs", "demo.xml")
        vfs.load(path)
        self.assertEqual(vfs.get_node("/home")["type"], "dir")
        self.assertEqual(vfs.get_node("/home/student/data.bin")["content"], b"\x00\x01\x02\x03\x04")

    def test_save(self):
        vfs = VirtualFileSystem()
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "saved.xml")
            vfs.save(path)
            self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
