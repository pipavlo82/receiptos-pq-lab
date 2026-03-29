from __future__ import annotations

from typing import Any, Dict


REQ_SIG_FIELDS = ("alg", "key_id", "sig")


def verify_signature_extension(ext: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, Any] = {}

    if ext.get("mode") != "signature_extension":
        return {
            "valid": False,
            "mode": ext.get("mode"),
            "reason_code": "MODE_FIELD_MISMATCH",
            "checks": {"mode_expected": "signature_extension", "mode_actual": ext.get("mode")},
            "fail_path": "receipt_extension.mode",
        }

    sig = ext.get("pq_signature")
    if not isinstance(sig, dict):
        mismatch = "entropy" in ext
        return {
            "valid": False,
            "mode": "signature_extension",
            "reason_code": "MODE_FIELD_MISMATCH" if mismatch else "MISSING_REQUIRED_FIELD",
            "checks": {"pq_signature_present": False},
            "fail_path": "receipt_extension.pq_signature",
        }

    missing = [k for k in REQ_SIG_FIELDS if not sig.get(k)]
    if missing:
        return {
            "valid": False,
            "mode": "signature_extension",
            "reason_code": "MISSING_REQUIRED_FIELD",
            "checks": {"missing": missing},
            "fail_path": "receipt_extension.pq_signature",
        }

    checks["pq_signature_present"] = True
    checks["alg"] = sig.get("alg")
    checks["key_id"] = sig.get("key_id")

    # deterministic mock behavior (no real PQ crypto):
    # any sig starting with "bad" fails.
    sig_val = str(sig.get("sig") or "")
    if sig_val.startswith("bad"):
        return {
            "valid": False,
            "mode": "signature_extension",
            "reason_code": "MOCK_SIGNATURE_INVALID",
            "checks": checks,
            "fail_path": "receipt_extension.pq_signature.sig",
        }

    return {
        "valid": True,
        "mode": "signature_extension",
        "reason_code": "OK",
        "checks": checks,
        "fail_path": None,
    }
