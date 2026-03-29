from __future__ import annotations

from typing import Any, Dict


SUPPORTED_SCHEMES = {"MLDSA-44", "MLDSA-65", "MLDSA-87", "MLDSA-STUB-V1"}


def verify_mldsa_stub(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic ML-DSA stub (no real cryptography).

    Expected input shape:
      {
        "scheme_id": str,
        "canonical_payload": str|dict (optional if canonical_digest exists),
        "canonical_digest": str (optional if canonical_payload exists),
        "public_key": str,
        "signature": str,
        "metadata": dict (optional)
      }

    Raw output shape:
      {
        "ok": bool,
        "raw_reason": str,
        "details": dict,
        "fail_path": str|None
      }
    """
    if not isinstance(payload, dict):
        return {
            "ok": False,
            "raw_reason": "invalid_input",
            "details": {"expected": "dict"},
            "fail_path": "payload",
        }

    required = ["scheme_id", "public_key", "signature"]
    missing = [k for k in required if not payload.get(k)]
    if missing:
        return {
            "ok": False,
            "raw_reason": "missing_required_field",
            "details": {"missing": missing},
            "fail_path": "payload",
        }

    if not payload.get("canonical_payload") and not payload.get("canonical_digest"):
        return {
            "ok": False,
            "raw_reason": "missing_required_field",
            "details": {"missing": ["canonical_payload|canonical_digest"]},
            "fail_path": "payload.canonical_payload",
        }

    scheme = str(payload.get("scheme_id"))
    if scheme not in SUPPORTED_SCHEMES:
        return {
            "ok": False,
            "raw_reason": "unsupported_scheme",
            "details": {"scheme_id": scheme, "supported": sorted(SUPPORTED_SCHEMES)},
            "fail_path": "payload.scheme_id",
        }

    pk = str(payload.get("public_key"))
    sig = str(payload.get("signature"))
    if not pk.startswith("mldsa_pk_") or not sig.startswith("mldsa_sig_"):
        return {
            "ok": False,
            "raw_reason": "invalid_placeholder_shape",
            "details": {
                "public_key_prefix_required": "mldsa_pk_",
                "signature_prefix_required": "mldsa_sig_",
            },
            "fail_path": "payload.public_key",
        }

    # deterministic mock verification outcome:
    # signatures containing "fail" are invalid.
    if "fail" in sig:
        return {
            "ok": False,
            "raw_reason": "signature_invalid",
            "details": {"scheme_id": scheme, "note": "stub-deterministic-failure"},
            "fail_path": "payload.signature",
        }

    return {
        "ok": True,
        "raw_reason": "ok",
        "details": {"scheme_id": scheme, "note": "stub-deterministic-pass"},
        "fail_path": None,
    }
