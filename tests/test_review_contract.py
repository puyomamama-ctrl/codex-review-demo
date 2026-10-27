"""Offline tests for strict Whis review contract. No API calls or secrets."""
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from review_contract import parse_review_response


class ReviewContractTests(unittest.TestCase):
    def parse(self, **overrides):
        item = {"task_id": "demo-1", "verdict": "approve", "findings": []}
        item.update(overrides)
        return parse_review_response(json.dumps(item), "demo-1")

    def test_approve(self):
        self.assertEqual(self.parse()["verdict"], "approve")

    def test_changes_requested(self):
        self.assertEqual(self.parse(
            verdict="changes_requested", findings=["Add tests"]
        )["findings"], ["Add tests"])

    def test_wrong_task_rejected(self):
        with self.assertRaises(ValueError):
            self.parse(task_id="other")

    def test_extra_fields_rejected(self):
        with self.assertRaises(ValueError):
            self.parse(command="execute-this")

    def test_approval_with_findings_rejected(self):
        with self.assertRaises(ValueError):
            self.parse(findings=["Risk"])

    def test_changes_without_findings_rejected(self):
        with self.assertRaises(ValueError):
            self.parse(verdict="changes_requested")

    def test_blank_finding_rejected(self):
        with self.assertRaises(ValueError):
            self.parse(verdict="changes_requested", findings=[" "])

    def test_oversized_payload_rejected(self):
        with self.assertRaises(ValueError):
            parse_review_response(" " * 12001, "demo-1")

    def test_too_many_findings_rejected(self):
        with self.assertRaises(ValueError):
            self.parse(verdict="changes_requested", findings=["risk"] * 21)

    def test_non_json_rejected(self):
        with self.assertRaises(ValueError):
            parse_review_response("{invalid", "demo-1")


if __name__ == "__main__":
    unittest.main()
