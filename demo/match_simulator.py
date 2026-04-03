#!/usr/bin/env python3
"""Deterministic match event simulator (std-lib only)."""
from __future__ import annotations

import json
from pathlib import Path


def build_match_events() -> list[dict]:
    return [
        {"event_id": 1, "payload": {"type": "match_start", "match_id": "m-001", "map": "arena"}},
        {"event_id": 2, "payload": {"type": "spawn", "player": "alice", "x": 10, "y": 5}},
        {"event_id": 3, "payload": {"type": "spawn", "player": "bob", "x": 4, "y": 8}},
        {"event_id": 4, "payload": {"type": "damage", "from": "alice", "to": "bob", "hp_delta": -40}},
        {"event_id": 5, "payload": {"type": "damage", "from": "bob", "to": "alice", "hp_delta": -20}},
        {"event_id": 6, "payload": {"type": "final_blow", "from": "alice", "to": "bob"}},
        {"event_id": 7, "payload": {"type": "match_end", "winner": "alice"}},
    ]


def main() -> None:
    out = Path(__file__).resolve().parents[1] / "data" / "match_events.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(build_match_events(), indent=2), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
