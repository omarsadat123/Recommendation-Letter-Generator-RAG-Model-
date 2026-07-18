"""Focused tests for scoring and level mapping helpers."""

from pathlib import Path
import sys
import unittest

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from lor_rag.app import extract_score, lor_level


class AppLogicTests(unittest.TestCase):
    def test_extract_score_with_rich_profile(self) -> None:
        text = "CGPA: 3.9\nAchievements: Winner\nSkills: Python\nResearch: NLP"
        self.assertGreaterEqual(extract_score(text), 8)

    def test_extract_score_without_signals(self) -> None:
        self.assertEqual(extract_score("No relevant fields"), 1)

    def test_lor_level_mapping(self) -> None:
        self.assertEqual(lor_level(9), "high")
        self.assertEqual(lor_level(7), "medium-high")
        self.assertEqual(lor_level(5), "medium")
        self.assertEqual(lor_level(3), "medium-low")
        self.assertEqual(lor_level(1), "low")


if __name__ == "__main__":
    unittest.main()
