from __future__ import annotations

from typing import Any, Dict, Protocol


class MLDSABackend(Protocol):
    """
    Narrow/stable backend contract for ML-DSA verification engines.

    verify(...) input:
      - canonical_payload_or_digest: str | dict
      - public_key: str
      - signature: str
      - metadata: dict

    verify(...) raw output (backend-local):
      {
        "ok": bool,
        "raw_reason": str,
        "details": dict
      }

    NOTE:
    - backend output is intentionally narrow
    - adapter layer is responsible for adding fail_path and public normalization
    - backend implementations must not leak raw exception strings outside adapter boundary
    """

    def verify(
        self,
        canonical_payload_or_digest: Any,
        public_key: str,
        signature: str,
        metadata: Dict[str, Any],
    ) -> Dict[str, Any]: ...


def sanitize_backend_exception(exc: Exception) -> Dict[str, Any]:
    """Convert backend exception to deterministic backend-local failure."""
    return {
        "ok": False,
        "raw_reason": "internal_error",
        "details": {
            "error_type": type(exc).__name__,
            "error": "backend_internal_error",
        },
    }
