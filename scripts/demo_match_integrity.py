#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from src.extension_verifier import verify_extension
from src.mldsa_historical_loader import load_mldsa_vector_raw, to_mldsa_adapter_payload_from_vector_raw


ROOT = Path(__file__).resolve().parents[1]
DEMO_DIR = ROOT / "examples" / "gaming" / "demo_match_integrity"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def payload_fingerprint(receipt: dict) -> str:
    payload = (receipt.get("game_event") or {}).get("payload") or {}
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def explain(reason_code: str, valid: bool) -> str:
    if valid:
        return "Valid event: integrity checks passed"
    mapping = {
        "HYBRID_PARTIAL_FAILURE": "One hybrid sub-path failed (signature/entropy)",
        "VERIFY_FAILED": "Verification failed for provided proof/signature path",
        "MISSING_REQUIRED_FIELD": "Required field is missing",
        "MODE_FIELD_MISMATCH": "Mode and provided fields do not align",
        "INVALID_EXTENSION_SCHEMA": "Extension schema/shape is invalid",
        "TAMPER_DETECTED_DEMO": "Payload differs for same receipt identity (demo tamper detection)",
        "CONTINUITY_MISMATCH": "Chain continuity mismatch detected",
    }
    return mapping.get(reason_code, "Verification failed with deterministic reason")


def continuity_check(prev_receipt: dict, next_receipt: dict) -> tuple[bool, str]:
    prev_hash = prev_receipt.get("core_receipt_ref")
    next_prev = (next_receipt.get("chain") or {}).get("prev_hash")
    if prev_hash and next_prev and prev_hash != next_prev:
        return False, "CONTINUITY_MISMATCH"
    return True, "OK"


def run_receipt(name: str, receipt: dict, baseline_receipt: dict | None = None):
    out = verify_extension(receipt)
    valid = bool(out.get("valid"))
    reason = out.get("reason_code")

    # Thin demo-level tamper signal: same receipt_id but different event payload fingerprint.
    if baseline_receipt and receipt.get("receipt_id") == baseline_receipt.get("receipt_id"):
        if payload_fingerprint(receipt) != payload_fingerprint(baseline_receipt):
            valid = False
            reason = "TAMPER_DETECTED_DEMO"

    print(f"[{name}] valid={valid} reason_code={reason} :: {explain(reason, valid)}")


def main():
    valid = load_json(DEMO_DIR / "valid_match_result_receipt.json")
    tampered = load_json(DEMO_DIR / "tampered_match_result_receipt.json")
    continuity_bad = load_json(DEMO_DIR / "invalid_continuity_match_result_receipt.json")

    print("=== Match Integrity Demo ===")
    run_receipt("valid", valid)
    run_receipt("tampered", tampered, baseline_receipt=valid)
    run_receipt("continuity_payload", continuity_bad)

    ok, rc = continuity_check(valid, continuity_bad)
    print(f"[continuity_check] valid={ok} reason_code={rc} :: {explain(rc, ok)}")

    raw = load_mldsa_vector_raw()
    raw_payload = to_mldsa_adapter_payload_from_vector_raw(raw)
    print(
        "[vector_raw] digest/pk/sig ready for adapter path; "
        f"metadata_keys={sorted(list(raw_payload.get('metadata', {}).keys()))[:6]}..."
    )


if __name__ == "__main__":
    main()
