#!/usr/bin/env python3
"""Verify receipt chains: PASS/FAIL with reason (std-lib only)."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def recompute(event_id: int, prev_hash: str, payload: dict) -> str:
    payload_s = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(f"{event_id}|{prev_hash}|{payload_s}".encode("utf-8")).hexdigest()


def verify_chain(chain: list[dict]) -> tuple[bool, str]:
    if not isinstance(chain, list) or not chain:
        return False, "invalid input: empty chain"

    seen = set()
    expected_prev = "GENESIS"
    expected_event_id = 1

    for i, e in enumerate(chain, start=1):
        for k in ("event_id", "prev_hash", "payload", "hash"):
            if k not in e:
                return False, f"continuity failed at event #{i}: missing field '{k}'"

        event_id = int(e["event_id"])
        prev_hash = str(e["prev_hash"])
        payload = e["payload"]
        stored_hash = str(e["hash"])

        if event_id in seen:
            return False, f"replay detected at event #{i}: duplicate event_id={event_id}"
        seen.add(event_id)

        if event_id != expected_event_id:
            return False, f"replay/broken order at event #{i}: expected event_id={expected_event_id}, got {event_id}"

        if prev_hash != expected_prev:
            return False, f"continuity broken at event #{i}: prev_hash mismatch"

        calc = recompute(event_id, prev_hash, payload)
        if calc != stored_hash:
            return False, f"tamper detected at event #{i}: hash mismatch"

        expected_prev = stored_hash
        expected_event_id += 1

    return True, "PASS — receipt chain valid (no tamper/replay/continuity breaks)"


def run_one(path: Path) -> tuple[bool, str]:
    chain = json.loads(path.read_text(encoding="utf-8"))
    ok, msg = verify_chain(chain)
    head = "PASS" if ok else "FAIL"
    print(f"{path.name}: {head} — {msg}")
    return ok, msg


def write_report(results: list[tuple[str, bool, str]], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Verification Report", "", "Case: Player claims match was manipulated.", ""]
    for name, ok, msg in results:
        lines.append(f"- `{name}`: {'PASS' if ok else 'FAIL'} — {msg}")
    lines += ["", "Conclusion:"]
    if any(not ok for _, ok, _ in results):
        lines.append("- Invalid chains are clearly rejected with human-readable reason.")
        lines.append("- This demo proves altered/replayed execution can be detected.")
    else:
        lines.append("- All tested chains were valid.")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data = root / "data"
    if len(sys.argv) >= 2 and sys.argv[1] != "all":
        run_one(Path(sys.argv[1]))
        return

    files = [
        data / "valid_receipt_chain.json",
        data / "tampered_event_chain.json",
        data / "replay_injected_chain.json",
    ]
    results = []
    for fp in files:
        ok, msg = run_one(fp)
        results.append((fp.name, ok, msg))
    write_report(results, root / "output" / "verification_report.md")


if __name__ == "__main__":
    main()
