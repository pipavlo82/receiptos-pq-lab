#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path


def digest(event_id, prev_hash, payload):
    payload_s = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    raw = f"{event_id}|{prev_hash}|{payload_s}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def make_valid(events):
    chain, prev = [], "GENESIS"
    for e in events:
        eid = int(e["event_id"])
        payload = e["payload"]
        h = digest(eid, prev, payload)
        chain.append({"event_id": eid, "prev_hash": prev, "payload": payload, "hash": h})
        prev = h
    return chain


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    events_fp = root / "match_events.json"
    if not events_fp.exists():
        raise SystemExit("run match_simulator.py first")

    events = json.loads(events_fp.read_text(encoding="utf-8"))
    valid = make_valid(events)

    tampered = json.loads(json.dumps(valid))
    tampered[3]["payload"]["hp_delta"] = -400  # tamper payload, keep old hash

    replay = json.loads(json.dumps(valid))
    replay.insert(4, json.loads(json.dumps(valid[3])))  # duplicate event

    (root / "valid_receipt_chain.json").write_text(json.dumps(valid, indent=2), encoding="utf-8")
    (root / "tampered_event_chain.json").write_text(json.dumps(tampered, indent=2), encoding="utf-8")
    (root / "replay_injected_chain.json").write_text(json.dumps(replay, indent=2), encoding="utf-8")
    print("generated valid/tampered/replay chains")
