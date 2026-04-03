#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path


def digest(event_id, prev_hash, payload):
    payload_s = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(f"{event_id}|{prev_hash}|{payload_s}".encode("utf-8")).hexdigest()


def verify(chain):
    seen = set()
    expected_prev = "GENESIS"
    expected_id = 1
    for i, e in enumerate(chain, start=1):
        for k in ("event_id", "prev_hash", "payload", "hash"):
            if k not in e:
                return False, f"continuity failed at event #{i}: missing {k}"
        eid = int(e["event_id"])
        if eid in seen:
            return False, f"replay detected at event #{i}: duplicate event_id={eid}"
        seen.add(eid)
        if eid != expected_id:
            return False, f"replay/broken order at event #{i}: expected event_id={expected_id}, got {eid}"
        if e["prev_hash"] != expected_prev:
            return False, f"continuity broken at event #{i}: prev_hash mismatch"
        calc = digest(eid, e["prev_hash"], e["payload"])
        if calc != e["hash"]:
            return False, f"tamper detected at event #{i}: hash mismatch"
        expected_prev = e["hash"]
        expected_id += 1
    return True, "PASS — receipt chain valid (no tamper/replay/continuity breaks)"


def run_file(fp):
    chain = json.loads(Path(fp).read_text(encoding="utf-8"))
    ok, msg = verify(chain)
    print(f"{Path(fp).name}: {'PASS' if ok else 'FAIL'} — {msg}")
    return ok, msg


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    if len(sys.argv) > 1 and sys.argv[1] != "all":
        run_file(sys.argv[1])
        raise SystemExit(0)

    files = [
        root / "valid_receipt_chain.json",
        root / "tampered_event_chain.json",
        root / "replay_injected_chain.json",
    ]
    out = ["# Verification Report", "", "Case: Player claims match was manipulated.", ""]
    for f in files:
        ok, msg = run_file(f)
        out.append(f"- `{f.name}`: {'PASS' if ok else 'FAIL'} — {msg}")
    out += ["", "Conclusion:", "- Invalid chains are rejected with explicit reason."]
    (root / "verification_report.md").write_text("\n".join(out) + "\n", encoding="utf-8")
