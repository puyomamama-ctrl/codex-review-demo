"""Offline mock of Beerus -> Whis -> Beerus review handoff. No API or writes.

The Whis responses below are fixtures, not actual Grok replies.
"""
import json
import unittest

from test_review_handoff import make_review_request, parse_review_response


def mock_whis(request: dict, verdict: str, findings: list[str]) -> str:
    """A deterministic stand-in for Whis; never calls xAI."""
    return json.dumps({
        "task_id": request["task_id"],
        "verdict": verdict,
        "findings": findings,
    })


class RoundtripDemoTests(unittest.TestCase):
    def test_approved_roundtrip(self):
        request = make_review_request("demo-approve", "+print('safe demo')")
        response = mock_whis(request, "approve", [])
        parsed = parse_review_response(response, request["task_id"])
        self.assertEqual(parsed["verdict"], "approve")

    def test_changes_requested_roundtrip(self):
        request = make_review_request("demo-revise", "+print('demo')")
        response = mock_whis(request, "changes_requested", ["Add a test"])
        parsed = parse_review_response(response, request["task_id"])
        self.assertEqual(parsed["findings"], ["Add a test"])
        self.assertNotEqual(parsed["verdict"], "approve")

    def test_cross_task_reply_is_rejected(self):
        original = make_review_request("demo-a", "+pass")
        unrelated = make_review_request("demo-b", "+pass")
        reply = mock_whis(unrelated, "approve", [])
        with self.assertRaises(ValueError):
            parse_review_response(reply, original["task_id"])


if __name__ == "__main__":
    unittest.main()
