"""Validate structured Whis reviews. Treat all model output as untrusted data."""
import json


def parse_review_response(payload: str, expected_task_id: str) -> dict:
    if not isinstance(payload, str) or len(payload) > 12000:
        raise ValueError("Invalid review payload size")
    result = json.loads(payload)
    if not isinstance(result, dict):
        raise ValueError("Expected a JSON object")
    if set(result) != {"task_id", "verdict", "findings"}:
        raise ValueError("Unexpected review fields")
    if result["task_id"] != expected_task_id:
        raise ValueError("Review task_id mismatch")
    if result["verdict"] not in ("approve", "changes_requested"):
        raise ValueError("Invalid review verdict")
    findings = result["findings"]
    if not isinstance(findings, list) or len(findings) > 20 or any(
        not isinstance(item, str) or not item.strip() or len(item) > 1000
        for item in findings
    ):
        raise ValueError("Invalid review findings")
    if result["verdict"] == "approve" and findings:
        raise ValueError("Approval must have no findings")
    if result["verdict"] == "changes_requested" and not findings:
        raise ValueError("Changes requested must include findings")
    return result
