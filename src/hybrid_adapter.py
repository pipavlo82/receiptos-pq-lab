from __future__ import annotations

from typing import Any, Dict

from .reason_mapping import normalize_exception
from .pq_signature_adapter import PQSignatureAdapter, verify_pq_signature_with_adapter
from .entropy_proof_adapter import EntropyProofAdapter, verify_entropy_proof_with_adapter


def verify_hybrid_with_adapters(
    extension: Dict[str, Any],
    pq_adapter: PQSignatureAdapter,
    entropy_adapter: EntropyProofAdapter,
) -> Dict[str, Any]:
    """
    Hybrid composition contract:
      - run pq adapter + entropy adapter over same extension envelope
      - normalize partial failures deterministically
      - keep unified output shape
    """
    try:
        if extension.get("mode") != "hybrid":
            return {
                "valid": False,
                "mode": extension.get("mode"),
                "reason_code": "MODE_FIELD_MISMATCH",
                "checks": {"raw_reason": "mode_field_mismatch", "details": {"mode": extension.get("mode")}},
                "fail_path": "receipt_extension.mode",
            }

        pq_res = verify_pq_signature_with_adapter(extension, pq_adapter)
        ent_res = verify_entropy_proof_with_adapter(extension, entropy_adapter)

        checks = {"pq": pq_res, "entropy": ent_res}

        if pq_res["valid"] and ent_res["valid"]:
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
                "pq": None if pq_res["valid"] else pq_res.get("fail_path"),
                "entropy": None if ent_res["valid"] else ent_res.get("fail_path"),
            },
        }
    except Exception as exc:
        return normalize_exception("hybrid", exc, "receipt_extension")
