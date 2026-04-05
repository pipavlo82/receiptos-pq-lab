#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List


def generate_additional_disputes(match: Dict[str, Any], receipts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Optional simulation-only scenario generator.
    Does NOT change verification logic.
    """
    out = []

    # Scenario: crowd-pressure modifies one early move heavily
    m1 = deepcopy(match)
    if m1.get("events"):
        m1["events"][0]["delta"] = int(m1["events"][0].get("delta", 1)) + 7
    out.append(
        {
            "case_id": "mirofish_pressure_tamper",
            "kind": "tamper",
            "description": "Simulated crowd-pressure narrative altered an early move delta.",
            "match": m1,
            "receipts": deepcopy(receipts),
        }
    )

    # Scenario: late replay burst injects duplicate final event receipt
    r2 = deepcopy(receipts)
    if r2:
        r2.append(deepcopy(r2[-1]))
    out.append(
        {
            "case_id": "mirofish_replay_burst",
            "kind": "replay",
            "description": "Simulated replay burst duplicates final receipt.",
            "match": deepcopy(match),
            "receipts": r2,
        }
    )

    return out
