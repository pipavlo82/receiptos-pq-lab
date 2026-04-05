#!/usr/bin/env python3
from __future__ import annotations

import argparse
import random
from datetime import datetime, timezone
from pathlib import Path

from _demo_lib import write_json


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_match(seed: int = 42, symbol: str = "XBTUSD"):
    rng = random.Random(seed)
    players = ["p1", "p2"]
    base = 100
    events = []
    score = {"p1": 0, "p2": 0}

    for i in range(1, 9):
        actor = players[i % 2]
        delta = rng.choice([1, 2, 3])
        score[actor] += delta
        price = round(base + rng.uniform(-2.0, 2.0), 4)
        events.append(
            {
                "event_id": f"ev_{i:03d}",
                "ts": now_iso(),
                "type": "move",
                "actor": actor,
                "delta": delta,
                "symbol": symbol,
                "mark_price": price,
                "score_after": dict(score),
            }
        )

    winner = "p1" if score["p1"] >= score["p2"] else "p2"
    events.append(
        {
            "event_id": "ev_999",
            "ts": now_iso(),
            "type": "result",
            "winner": winner,
            "final_score": score,
            "symbol": symbol,
        }
    )

    return {
        "match_id": f"match_{seed}",
        "seed": seed,
        "symbol": symbol,
        "created_at": now_iso(),
        "events": events,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Generate deterministic match state for demo")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--symbol", default="XBTUSD")
    p.add_argument("--output", default="artifacts/demo_run/match.json")
    args = p.parse_args()

    match = build_match(seed=args.seed, symbol=args.symbol)
    write_json(Path(args.output), match)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
