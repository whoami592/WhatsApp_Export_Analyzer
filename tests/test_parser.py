import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from parser import parse_export, statistics


class ParserTests(unittest.TestCase):
    def test_parse_and_multiline(self):
        data = "17/09/2026, 9:15 PM - Sabaz: Hello\ncontinued\n17/09/2026, 9:16 PM - User: Hi"
        messages = parse_export(data)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0].text, "Hello\ncontinued")
        self.assertEqual(statistics(messages)["participants"], 2)


if __name__ == "__main__":
    unittest.main()
