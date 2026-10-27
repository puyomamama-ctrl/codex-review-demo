"""Offline contract test for the Beerus ↔ Whis review handoff.

No network calls, API credentials, external packages or file writes.
"""
import json
import unittest


def make_review_request(task_id: str, diff: str) -> dict:
    if not task_id.strip() or not diff.strip():
        raise ValueError("task_id and diff must be non-empty")
    return {
        "schema_version": 1,
        "task_id": task_id,
        "reviewer": "whis",
        "instructions": "Review the proposed change. Do not execute it. Return risks and suggested tests.",
        "diff": diff,
    }


def parse_review_response(payload: str, expected_task_id: str) -> dict:
    result = json.loads(payload)
    if not isinstance(result, dict):
        raise ValueError("Expected a JSON object")
    if result.get("task_id") != expected_task_id:
        raise ValueError("Review task_id mismatch")
    if result.get("verdict") not in ("approve", "changes_requested"):
        raise ValueError("Invalid review verdict")
    if not isinstance(result.get("findings"), list) or not all(
        isinstance(item, str) for item in result["findings"]
    ):
        raise ValueError("findings must be a list of strings")
    return result


class HandoffTests(unittest.TestCase):
    def test_request(self):
        request = make_review_request("demo-1", "+print('hello')")
        self.assertEqual(request["reviewer"], "whis")
        self.assertEqual(request["schema_version"], 1)

    def test_empty_diff_rejected(self):
        with self.assertRaises(ValueError):
            make_review_request("demo-1", " ")

    def test_valid_review(self):
        response = json.dumps({
            "task_id": "demo-1", "verdict": "changes_requested",
            "findings": ["Add a regression test"],
        })
        self.assertEqual(parse_review_response(response, "demo-1")["findings"][0],
                         "Add a regression test")

    def test_mismatched_task_rejected(self):
        response = json.dumps({
            "task_id": "other", "verdict": "approve", "findings": [],
        })
        with self.assertRaises(ValueError):
            parse_review_response(response, "demo-1")


if __name__ == "__main__":
    unittest.main()
