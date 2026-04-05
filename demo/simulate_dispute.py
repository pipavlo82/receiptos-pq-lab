#!/usr/bin/env python3
from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path

from _demo_lib import read_json, write_json


def build_disputes(match, receipts, with_mirofish=False):
    cases = []

    # valid baseline
    cases.append(
        {
            "case_id": "valid_baseline",
            "kind": "valid",
            "description": "Untouched match + untouched receipts",
            "match": deepcopy(match),
            "receipts": deepcopy(receipts),
        }
    )

    # tamper: alter event payload only
    tampered_match = deepcopy(match)
    if tampered_match.get("events"):
        tampered_match["events"][3]["delta"] = int(tampered_match["events"][3].get("delta", 1)) + 4
    cases.append(
        {
            "case_id": "tamper_event",
            "kind": "tamper",
            "description": "Event payload modified after receipt signing",
            "match": tampered_match,
            "receipts": deepcopy(receipts),
        }
    )

    # replay: duplicate one receipt
    replay_receipts = deepcopy(receipts)
    if replay_receipts:
        replay_receipts.insert(5, deepcopy(replay_receipts[2]))
    cases.append(
        {
            "case_id": "replay_receipt",
            "kind": "replay",
            "description": "Duplicated receipt/event id in chain",
            "match": deepcopy(match),
            "receipts": replay_receipts,
        }
    )

    # altered result
    altered_result = deepcopy(match)
    if altered_result.get("events"):
        altered_result["events"][-1]["winner"] = "p2" if altered_result["events"][-1].get("winner") == "p1" else "p1"
    cases.append(
        {
            "case_id": "altered_result",
            "kind": "tamper",
            "description": "Final winner altered after signing",
            "match": altered_result,
            "receipts": deepcopy(receipts),
        }
    )

    # bad signature
    bad_sig = deepcopy(receipts)
    if bad_sig:
        bad_sig[1]["signature"] = "00bad00signature"
    cases.append(
        {
            "case_id": "bad_signature",
            "kind": "bad_signature",
            "description": "Receipt signature corrupted",
            "match": deepcopy(match),
            "receipts": bad_sig,
        }
    )

    # chain mismatch
    bad_chain = deepcopy(receipts)
    if bad_chain:
        bad_chain[2]["prev_hash"] = "BROKEN_PREV_HASH"
    cases.append(
        {
            "case_id": "chain_mismatch",
            "kind": "chain_mismatch",
            "description": "prev_hash continuity broken",
            "match": deepcopy(match),
            "receipts": bad_chain,
        }
    )

    if with_mirofish:
        from mirofish_scenarios import generate_additional_disputes

        cases.extend(generate_additional_disputes(match, receipts))

    return {"with_mirofish": with_mirofish, "cases": cases}


def main() -> int:
    p = argparse.ArgumentParser(description="Build dispute scenarios")
    p.add_argument("--match", default="artifacts/demo_run/match.json")
    p.add_argument("--receipts", default="artifacts/demo_run/receipts_chain.json")
    p.add_argument("--output", default="artifacts/demo_run/disputes.json")
    p.add_argument("--with-mirofish", action="store_true")
    args = p.parse_args()

    match = read_json(Path(args.match))
    receipts = read_json(Path(args.receipts))
    disputes = build_disputes(match, receipts, with_mirofish=args.with_mirofish)
    write_json(Path(args.output), disputes)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
