import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from emulator.parser import ParseError, parse_command


class ParserTests(unittest.TestCase):
    def test_quotes(self):
        self.assertEqual(parse_command('cd "My Folder"'), ["cd", "My Folder"])

    def test_unclosed_quote(self):
        with self.assertRaises(ParseError):
            parse_command('cd "broken')


if __name__ == "__main__":
    unittest.main()
