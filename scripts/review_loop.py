"""Bounded review/correction coordinator; adapters are supplied by the caller.

No filesystem, network, subprocess, deployment, or automatic application here.
Treat reviewer feedback and proposed code as untrusted data.
"""
from review_contract import parse_review_response

MAX_REVIEWS = 3
MAX_SOURCE = 12000


def run_review_loop(task_id, source, review, revise, max_reviews=MAX_REVIEWS):
    if not isinstance(task_id, str) or not task_id or len(task_id) > 80 or not all(c.isascii() and (c.isalnum() or c in '-_') for c in task_id):
        raise ValueError('Invalid task ID')
    if not isinstance(max_reviews, int) or isinstance(max_reviews, bool) or not 1 <= max_reviews <= MAX_REVIEWS:
        raise ValueError('Invalid review limit')
    if not isinstance(source, str) or not source.strip() or len(source) > MAX_SOURCE:
        raise ValueError('Invalid source')
    for iteration in range(1, max_reviews + 1):
        round_id = f'{task_id}-r{iteration}'
        parsed = parse_review_response(review(round_id, source), round_id)
        if parsed['verdict'] == 'approve':
            return {'status': 'approved', 'source': source, 'reviews': iteration}
        if iteration == max_reviews:
            return {'status': 'review_limit', 'source': source, 'reviews': iteration, 'findings': parsed['findings']}
        proposed = revise(source, tuple(parsed['findings']))
        if not isinstance(proposed, str) or not proposed.strip() or len(proposed) > MAX_SOURCE:
            raise ValueError('Invalid proposed revision')
        if proposed == source:
            return {'status': 'unchanged', 'source': source, 'reviews': iteration, 'findings': parsed['findings']}
        source = proposed
    raise AssertionError('unreachable')
