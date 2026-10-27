"""Deterministic offline tests: neither callback executes code or contacts APIs."""
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from review_loop import run_review_loop


def response(task_id, verdict, findings):
    return json.dumps({'task_id': task_id, 'verdict': verdict, 'findings': findings})


class LoopTests(unittest.TestCase):
    def test_changes_then_approval_reviews_new_revision(self):
        calls = []
        def review(task, source):
            calls.append((task, source))
            return response(task, 'changes_requested', ['Add a test']) if len(calls) == 1 else response(task, 'approve', [])
        def revise(source, findings):
            self.assertEqual(findings, ('Add a test',))
            return source + '\n# fixed'
        result = run_review_loop('demo', 'initial', review, revise)
        self.assertEqual(result['status'], 'approved')
        self.assertEqual(calls, [('demo-r1', 'initial'), ('demo-r2', 'initial\n# fixed')])

    def test_limit_stops_without_an_extra_revision(self):
        fixes = []
        def revise(source, findings):
            fixes.append(1)
            return source + 'x'
        result = run_review_loop('demo', 'initial', lambda task, source: response(task, 'changes_requested', ['risk']), revise, max_reviews=2)
        self.assertEqual(result['status'], 'review_limit')
        self.assertEqual(len(fixes), 1)

    def test_wrong_or_malformed_review_never_reaches_reviser(self):
        for payload in ('not json', response('wrong-r1', 'approve', [])):
            with self.subTest(payload=payload):
                def revise(*args):
                    self.fail('must not revise')
                with self.assertRaises(ValueError):
                    run_review_loop('demo', 'initial', lambda *args: payload, revise)

    def test_unchanged_revision_stops(self):
        result = run_review_loop('demo', 'initial', lambda task, source: response(task, 'changes_requested', ['risk']), lambda source, findings: source)
        self.assertEqual(result['status'], 'unchanged')

    def test_invalid_revision_rejected(self):
        with self.assertRaises(ValueError):
            run_review_loop('demo', 'initial', lambda task, source: response(task, 'changes_requested', ['risk']), lambda *args: '')

if __name__ == '__main__':
    unittest.main()
