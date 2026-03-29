from __future__ import annotations

from typing import Any, Dict


REQ_ENT_FIELDS = ("entropy_score", "entropy_source", "freshness_window_sec")


def verify_entropy_proof(ext: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, Any] = {}

    if ext.get("mode") != "entropy_proof":
        return {
            "valid": False,
            "mode": ext.get("mode"),
            "reason_code": "MODE_FIELD_MISMATCH",
            "checks": {"mode_expected": "entropy_proof", "mode_actual": ext.get("mode")},
            "fail_path": "receipt_extension.mode",
        }

    ent = ext.get("entropy")
    if not isinstance(ent, dict):
        mismatch = "pq_signature" in ext
        return {
            "valid": False,
            "mode": "entropy_proof",
            "reason_code": "MODE_FIELD_MISMATCH" if mismatch else "MISSING_REQUIRED_FIELD",
            "checks": {"entropy_present": False},
            "fail_path": "receipt_extension.entropy",
        }

    missing = [k for k in REQ_ENT_FIELDS if ent.get(k) is None or ent.get(k) == ""]
    if missing:
        return {
            "valid": False,
            "mode": "entropy_proof",
            "reason_code": "MISSING_REQUIRED_FIELD",
            "checks": {"missing": missing},
            "fail_path": "receipt_extension.entropy",
        }

    try:
        score = float(ent.get("entropy_score"))
    except Exception:
        return {
            "valid": False,
            "mode": "entropy_proof",
            "reason_code": "INVALID_EXTENSION_SCHEMA",
            "checks": {"entropy_score_type": str(type(ent.get("entropy_score")))},
            "fail_path": "receipt_extension.entropy.entropy_score",
        }

    try:
        freshness = int(ent.get("freshness_window_sec"))
    except Exception:
        return {
            "valid": False,
            "mode": "entropy_proof",
            "reason_code": "INVALID_EXTENSION_SCHEMA",
            "checks": {"freshness_type": str(type(ent.get("freshness_window_sec")))},
            "fail_path": "receipt_extension.entropy.freshness_window_sec",
        }

    checks["entropy_score"] = score
    checks["freshness_window_sec"] = freshness

    if not (0.0 <= score <= 1.0):
        return {
            "valid": False,
            "mode": "entropy_proof",
            "reason_code": "MOCK_ENTROPY_INVALID",
            "checks": checks,
            "fail_path": "receipt_extension.entropy.entropy_score",
        }

    if freshness <= 0:
        return {
            "valid": False,
            "mode": "entropy_proof",
            "reason_code": "MOCK_ENTROPY_INVALID",
            "checks": checks,
            "fail_path": "receipt_extension.entropy.freshness_window_sec",
        }

    return {
        "valid": True,
        "mode": "entropy_proof",
        "reason_code": "OK",
        "checks": checks,
        "fail_path": None,
    }
