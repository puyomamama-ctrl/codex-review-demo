"""Offline tests for the fixed structured-review prompt."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from review_prompt import TASK_ID, review_instructions


class ReviewPromptTests(unittest.TestCase):
    def test_requires_exact_json_contract(self):
        prompt = review_instructions()
        for phrase in ("ONLY a JSON object", "task_id", "verdict", "findings",
                       "approve", "changes_requested", "Never execute"):
            self.assertIn(phrase, prompt)

    def test_task_id_is_fixed(self):
        self.assertIn(TASK_ID, review_instructions())

    def test_invalid_task_id_rejected(self):
        with self.assertRaises(ValueError):
            review_instructions("bad id / nope")


if __name__ == "__main__":
    unittest.main()
