"""Test the real one-shot handoff without network access or credentials."""
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import whis_review_once as runner


class Response(io.BytesIO):
    pass


class OneShotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.source = root / "demo.py"
        self.source.write_text("print('demo')", encoding="utf-8")
        self.output = root / "review.json"
        self.patches = [patch.object(runner, "SOURCE", self.source),
                        patch.object(runner, "OUTPUT", self.output),
                        patch.dict(os.environ, {"XAI_API_KEY": "fake-key", "XAI_MODEL": "fake-model"})]
        for item in self.patches:
            item.start()
            self.addCleanup(item.stop)

    def run_with(self, answer):
        response = json.dumps({"choices": [{"message": {"content": answer}}]}).encode()
        with patch.object(runner.urllib.request, "urlopen", return_value=Response(response)):
            return runner.main()

    def test_valid_review_saved(self):
        answer = json.dumps({"task_id": runner.TASK_ID, "verdict": "changes_requested", "findings": ["Add test"]})
        self.assertEqual(self.run_with(answer), 0)
        self.assertEqual(json.loads(self.output.read_text())["findings"], ["Add test"])

    def test_invalid_reviews_never_saved_and_stale_output_removed(self):
        for answer in ("not json", json.dumps({"task_id": runner.TASK_ID, "verdict": "approve", "findings": [123]}),
                       json.dumps({"task_id": "wrong", "verdict": "approve", "findings": []})):
            with self.subTest(answer=answer):
                self.output.write_text("stale")
                self.assertEqual(self.run_with(answer), 1)
                self.assertFalse(self.output.exists())

    def test_network_failure_removes_stale_output(self):
        self.output.write_text("stale")
        with patch.object(runner.urllib.request, "urlopen", side_effect=runner.urllib.error.URLError("offline")):
            self.assertEqual(runner.main(), 1)
        self.assertFalse(self.output.exists())

    def test_oversized_api_response_rejected(self):
        with patch.object(runner.urllib.request, "urlopen", return_value=Response(b"x" * (runner.MAX_RESPONSE_BYTES + 1))):
            self.assertEqual(runner.main(), 1)
        self.assertFalse(self.output.exists())

if __name__ == "__main__":
    unittest.main()
