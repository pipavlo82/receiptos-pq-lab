from __future__ import annotations

from typing import Any, Dict, Protocol

from .mldsa_adapter_stub import verify_mldsa_stub
from .reason_mapping import normalize_adapter_output, normalize_exception, normalize_result


class PQSignatureAdapter(Protocol):
    """
    Stable adapter contract for future PQ signature implementations.

    Input payload shape:
      {
        "scheme_id": str,
        "canonical_payload": str|dict (optional if canonical_digest exists),
        "canonical_digest": str (optional if canonical_payload exists),
        "public_key": str,
        "signature": str,
        "metadata": dict (optional)
      }

    Adapter raw return shape:
      {
        "ok": bool,
        "raw_reason": str,
        "details": dict,
        "fail_path": str|None
      }
    """

    def verify(self, payload: Dict[str, Any]) -> Dict[str, Any]: ...


class MLDSAAdapterStub:
    """Stub adapter wrapping deterministic ML-DSA placeholder verifier."""

    def verify(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return verify_mldsa_stub(payload)


def build_pq_payload_from_extension(extension: Dict[str, Any]) -> Dict[str, Any]:
    """
    Adapter payload builder from extension envelope, preserving current integration shape.
    Does not change schema direction; simply projects extension fields into adapter contract.
    """
    pq = extension.get("pq_signature") or {}
    return {
        "scheme_id": pq.get("alg") or extension.get("scheme_id") or "",
        "canonical_payload": extension.get("canonical_payload"),
        "canonical_digest": extension.get("canonical_digest"),
        "public_key": pq.get("public_key") or pq.get("pub_ref") or "",
        "signature": pq.get("sig") or "",
        "metadata": {
            "mode": extension.get("mode"),
            "key_id": pq.get("key_id"),
            "policy_path": extension.get("policy_path"),
        },
    }


def verify_pq_signature_contract(payload: Dict[str, Any], adapter: PQSignatureAdapter) -> Dict[str, Any]:
    """
    Adapter-contract normalized output requested for PQ layer:
      { valid, adapter_result, adapter_reason, normalized_reason_code, details }
    """
    try:
        raw = adapter.verify(payload)
        return normalize_adapter_output(raw)
    except Exception as exc:
        base = normalize_exception("signature_extension", exc, "payload")
        return {
            "valid": False,
            "adapter_result": "fail",
            "adapter_reason": "internal_error",
            "normalized_reason_code": base["reason_code"],
            "details": base["checks"]["details"],
        }


def verify_pq_signature_with_adapter(extension: Dict[str, Any], adapter: PQSignatureAdapter) -> Dict[str, Any]:
    """
    Compatibility wrapper for existing integration shape:
      { valid, mode, reason_code, checks, fail_path }
    while also exposing adapter-contract fields.
    """
    payload = build_pq_payload_from_extension(extension)
    try:
        raw = adapter.verify(payload)
        unified = normalize_result("signature_extension", raw)
        contract_out = normalize_adapter_output(raw)
        unified.update(contract_out)
        return unified
    except Exception as exc:
        unified = normalize_exception("signature_extension", exc, "receipt_extension.pq_signature")
        unified.update(
            {
                "adapter_result": "fail",
                "adapter_reason": "internal_error",
                "normalized_reason_code": unified["reason_code"],
                "details": unified["checks"]["details"],
            }
        )
        return unified
