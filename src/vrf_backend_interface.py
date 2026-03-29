from __future__ import annotations

from typing import Any, Dict, Protocol


class VRFBackend(Protocol):
    """
    Narrow/stable backend contract for VRF/entropy proof verification.

    verify(...) input:
      - entropy_proof_payload: dict
      - metadata: dict

    verify(...) raw output (backend-local):
      {
        "ok": bool,
        "raw_reason": str,
        "details": dict
      }

    Adapter layer handles fail_path + public normalization.
    """

    def verify(self, entropy_proof_payload: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]: ...


def sanitize_backend_exception(exc: Exception) -> Dict[str, Any]:
    return {
        "ok": False,
        "raw_reason": "internal_error",
        "details": {
            "error_type": type(exc).__name__,
            "error": "backend_internal_error",
        },
    }
