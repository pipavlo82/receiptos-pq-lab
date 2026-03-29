from __future__ import annotations

from typing import Any, Dict

# Normalized public reason codes (stable external surface)
OK = "OK"
ADAPTER_INVALID_INPUT = "ADAPTER_INVALID_INPUT"
ADAPTER_UNSUPPORTED_SCHEME = "ADAPTER_UNSUPPORTED_SCHEME"
ADAPTER_INTERNAL_ERROR = "ADAPTER_INTERNAL_ERROR"
MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
VERIFY_FAILED = "VERIFY_FAILED"
HYBRID_PARTIAL_FAILURE = "HYBRID_PARTIAL_FAILURE"
MODE_FIELD_MISMATCH = "MODE_FIELD_MISMATCH"
UNSUPPORTED_MODE = "UNSUPPORTED_MODE"


RAW_TO_NORMALIZED = {
    "ok": OK,
    "missing_required_field": MISSING_REQUIRED_FIELD,
    "invalid_input": ADAPTER_INVALID_INPUT,
    "invalid_placeholder_shape": ADAPTER_INVALID_INPUT,
    "unsupported_scheme": ADAPTER_UNSUPPORTED_SCHEME,
    "mode_field_mismatch": MODE_FIELD_MISMATCH,
    "unsupported_mode": UNSUPPORTED_MODE,
    "signature_invalid": VERIFY_FAILED,
    "entropy_invalid": VERIFY_FAILED,
    "verify_failed": VERIFY_FAILED,
    "hybrid_partial_failure": HYBRID_PARTIAL_FAILURE,
    "internal_error": ADAPTER_INTERNAL_ERROR,
    "adapter_unavailable": ADAPTER_INTERNAL_ERROR,
}


def map_raw_reason(raw_reason: str | None) -> str:
    if not raw_reason:
        return ADAPTER_INTERNAL_ERROR
    return RAW_TO_NORMALIZED.get(raw_reason, ADAPTER_INTERNAL_ERROR)


def normalize_adapter_output(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Adapter-level normalized shape (for PQ adapter contract):
    {
      valid,
      adapter_result,
      adapter_reason,
      normalized_reason_code,
      details
    }
    """
    valid = bool(raw.get("ok"))
    adapter_reason = str(raw.get("raw_reason") or "internal_error")
    return {
        "valid": valid,
        "adapter_result": "pass" if valid else "fail",
        "adapter_reason": adapter_reason,
        "normalized_reason_code": map_raw_reason(adapter_reason),
        "details": raw.get("details", {}),
    }


def normalize_result(mode: str, raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Legacy/unified verification shape used by extension verifier/hybrid composition:
      { valid, mode, reason_code, checks, fail_path }
    """
    core = normalize_adapter_output(raw)
    return {
        "valid": core["valid"],
        "mode": mode,
        "reason_code": core["normalized_reason_code"],
        "checks": {
            "raw_reason": core["adapter_reason"],
            "details": core["details"],
        },
        "fail_path": raw.get("fail_path"),
    }


def normalize_exception(mode: str, exc: Exception, fail_path: str | None = None) -> Dict[str, Any]:
    """
    Deterministic exception normalization.
    Do not leak raw exception strings publicly.
    """
    _ = exc
    return {
        "valid": False,
        "mode": mode,
        "reason_code": ADAPTER_INTERNAL_ERROR,
        "checks": {
            "raw_reason": "internal_error",
            "details": {
                "error_type": type(exc).__name__,
                "error": "internal_adapter_error",
            },
        },
        "fail_path": fail_path,
    }
