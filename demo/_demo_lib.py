#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import hmac
import json
from pathlib import Path
from typing import Any, Dict, List

DEMO_SECRET = b"receiptos-demo-secret-v1"


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sign_event_hash(event_hash: str, secret: bytes = DEMO_SECRET) -> str:
    return hmac.new(secret, event_hash.encode("utf-8"), hashlib.sha256).hexdigest()


def make_receipts(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    receipts: List[Dict[str, Any]] = []
    prev_hash = "GENESIS"
    for i, ev in enumerate(events, start=1):
        event_hash = sha256_hex(canonical(ev))
        signature = sign_event_hash(event_hash)
        rec = {
            "seq": i,
            "event_id": ev["event_id"],
            "event_hash": event_hash,
            "signature": signature,
            "prev_hash": prev_hash,
        }
        rec_hash = sha256_hex(canonical(rec))
        rec["receipt_hash"] = rec_hash
        receipts.append(rec)
        prev_hash = rec_hash
    return receipts


def verify_case(match: Dict[str, Any], receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
    events_by_id = {e["event_id"]: e for e in match.get("events", [])}

    seen_event_ids = set()
    prev_hash = "GENESIS"

    for idx, rec in enumerate(receipts, start=1):
        rid = rec.get("event_id")
        if rid in seen_event_ids:
            return {"ok": False, "reason_code": "REPLAY", "at_seq": idx, "details": f"duplicate event_id={rid}"}
        seen_event_ids.add(rid)

        if rec.get("prev_hash") != prev_hash:
            return {
                "ok": False,
                "reason_code": "CHAIN_MISMATCH",
                "at_seq": idx,
                "details": f"expected prev_hash={prev_hash}, got={rec.get('prev_hash')}",
            }

        ev = events_by_id.get(rid)
        if not ev:
            return {"ok": False, "reason_code": "TAMPER", "at_seq": idx, "details": f"missing event for id={rid}"}

        expected_event_hash = sha256_hex(canonical(ev))
        if expected_event_hash != rec.get("event_hash"):
            return {
                "ok": False,
                "reason_code": "TAMPER",
                "at_seq": idx,
                "details": "event_hash mismatch (event altered)",
            }

        expected_sig = sign_event_hash(expected_event_hash)
        if expected_sig != rec.get("signature"):
            return {
                "ok": False,
                "reason_code": "BAD_SIGNATURE",
                "at_seq": idx,
                "details": "signature mismatch",
            }

        # receipt hash integrity check
        base = {k: rec[k] for k in ["seq", "event_id", "event_hash", "signature", "prev_hash"]}
        expected_receipt_hash = sha256_hex(canonical(base))
        if expected_receipt_hash != rec.get("receipt_hash"):
            return {
                "ok": False,
                "reason_code": "CHAIN_MISMATCH",
                "at_seq": idx,
                "details": "receipt_hash mismatch",
            }

        prev_hash = rec.get("receipt_hash")

    return {"ok": True, "reason_code": "OK", "at_seq": None, "details": "all checks passed"}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
