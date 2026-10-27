"""One-shot Whis review of a fixed, public demo file. Never send secrets."""
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request

from review_contract import parse_review_response
from review_prompt import TASK_ID, review_instructions

SOURCE = Path("tests/test_review_handoff.py")
OUTPUT = Path("whis-review.json")
MAX_SOURCE = 12000
MAX_RESPONSE_BYTES = 65536


def main():
    # Never leave a previous success available after a failed attempt.
    OUTPUT.unlink(missing_ok=True)
    key = os.environ.get("XAI_API_KEY", "")
    model = os.environ.get("XAI_MODEL", "")
    if not key or not model:
        print("Missing secret or model selection")
        return 1
    try:
        source = SOURCE.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        print("Cannot read demo source")
        return 1
    if len(source) > MAX_SOURCE:
        print("Demo source too large")
        return 1
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": review_instructions()},
            {"role": "user", "content": "Review this fixed demo file, without running it:\n" + source},
        ],
        "max_tokens": 700,
        "stream": False,
    }
    req = urllib.request.Request(
        "https://api.x.ai/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read(MAX_RESPONSE_BYTES + 1)
        if len(raw) > MAX_RESPONSE_BYTES:
            raise ValueError("Response too large")
        data = json.loads(raw)
        answer = data["choices"][0]["message"]["content"]
        review = parse_review_response(answer, TASK_ID)
    except urllib.error.HTTPError as exc:
        print("xAI request failed, HTTP", exc.code)
        return 1
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, KeyError, IndexError, TypeError):
        print("xAI request failed or review did not meet the contract")
        return 1
    try:
        OUTPUT.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError:
        OUTPUT.unlink(missing_ok=True)
        print("Could not save validated review")
        return 1
    print("Validated Whis review saved as a workflow artifact")
    return 0

if __name__ == "__main__":
    sys.exit(main())
