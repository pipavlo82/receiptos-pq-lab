#!/usr/bin/env python3
"""Generate valid + tampered + replay receipt chains."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def h(event_id: int, prev_hash: str, payload: dict) -> str:
    payload_s = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    raw = f"{event_id}|{prev_hash}|{payload_s}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def load_events(data_dir: Path) -> list[dict]:
    fp = data_dir / "match_events.json"
    if fp.exists():
        return json.loads(fp.read_text(encoding="utf-8"))
    # fallback to deterministic defaults if simulator not run yet
    return [
        {"event_id": 1, "payload": {"type": "match_start", "match_id": "m-001", "map": "arena"}},
        {"event_id": 2, "payload": {"type": "spawn", "player": "alice", "x": 10, "y": 5}},
        {"event_id": 3, "payload": {"type": "spawn", "player": "bob", "x": 4, "y": 8}},
        {"event_id": 4, "payload": {"type": "damage", "from": "alice", "to": "bob", "hp_delta": -40}},
        {"event_id": 5, "payload": {"type": "damage", "from": "bob", "to": "alice", "hp_delta": -20}},
        {"event_id": 6, "payload": {"type": "final_blow", "from": "alice", "to": "bob"}},
        {"event_id": 7, "payload": {"type": "match_end", "winner": "alice"}},
    ]


def make_valid(events: list[dict]) -> list[dict]:
    chain = []
    prev = "GENESIS"
    for e in events:
        event_id = int(e["event_id"])
        payload = e["payload"]
        cur = h(event_id, prev, payload)
        chain.append({"event_id": event_id, "prev_hash": prev, "payload": payload, "hash": cur})
        prev = cur
    return chain


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data = root / "data"
    data.mkdir(parents=True, exist_ok=True)

    events = load_events(data)
    valid = make_valid(events)

    tampered = json.loads(json.dumps(valid))
    tampered[3]["payload"]["hp_delta"] = -400  # changed payload, hash unchanged -> tamper

    replay = json.loads(json.dumps(valid))
    replay.insert(4, json.loads(json.dumps(valid[3])))  # duplicate event in chain

    (data / "valid_receipt_chain.json").write_text(json.dumps(valid, indent=2), encoding="utf-8")
    (data / "tampered_event_chain.json").write_text(json.dumps(tampered, indent=2), encoding="utf-8")
    (data / "replay_injected_chain.json").write_text(json.dumps(replay, indent=2), encoding="utf-8")
    print("generated: valid_receipt_chain.json, tampered_event_chain.json, replay_injected_chain.json")


if __name__ == "__main__":
    main()
