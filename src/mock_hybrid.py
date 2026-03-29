from __future__ import annotations

from typing import Any, Dict

from .mock_signature_extension import verify_signature_extension
from .mock_entropy_proof import verify_entropy_proof


def verify_hybrid(ext: Dict[str, Any]) -> Dict[str, Any]:
    if ext.get("mode") != "hybrid":
        return {
            "valid": False,
            "mode": ext.get("mode"),
            "reason_code": "MODE_FIELD_MISMATCH",
            "checks": {"mode_expected": "hybrid", "mode_actual": ext.get("mode")},
            "fail_path": "receipt_extension.mode",
        }

    # Reuse verifiers by adapting mode for component checks.
    sig_in = dict(ext)
    sig_in["mode"] = "signature_extension"
    ent_in = dict(ext)
    ent_in["mode"] = "entropy_proof"

    sig_res = verify_signature_extension(sig_in)
    ent_res = verify_entropy_proof(ent_in)

    checks = {
        "signature_check": sig_res,
        "entropy_check": ent_res,
    }

    if sig_res.get("valid") and ent_res.get("valid"):
        return {
            "valid": True,
            "mode": "hybrid",
            "reason_code": "OK",
            "checks": checks,
            "fail_path": None,
        }

    return {
        "valid": False,
        "mode": "hybrid",
        "reason_code": "HYBRID_PARTIAL_FAILURE",
        "checks": checks,
        "fail_path": {
            "signature": None if sig_res.get("valid") else sig_res.get("fail_path"),
            "entropy": None if ent_res.get("valid") else ent_res.get("fail_path"),
        },
    }
