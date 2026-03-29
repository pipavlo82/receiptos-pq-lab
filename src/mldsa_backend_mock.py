from __future__ import annotations

from typing import Any, Dict

from .mldsa_backend_interface import sanitize_backend_exception


class MockMLDSABackend:
    """Deterministic backend mock for integration-boundary testing."""

    def verify(
        self,
        canonical_payload_or_digest: Any,
        public_key: str,
        signature: str,
        metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        try:
            if metadata.get("simulate") == "backend_unavailable":
                return {
                    "ok": False,
                    "raw_reason": "adapter_unavailable",
                    "details": {"source": "mock_backend"},
                }

            if metadata.get("simulate") == "internal_failure":
                raise RuntimeError("simulated backend failure")

            if canonical_payload_or_digest in (None, "", {}):
                return {
                    "ok": False,
                    "raw_reason": "missing_required_field",
                    "details": {"field": "canonical_payload_or_digest"},
                }

            if not isinstance(public_key, str) or not isinstance(signature, str):
                return {
                    "ok": False,
                    "raw_reason": "invalid_input",
                    "details": {"field": "public_key|signature"},
                }

            if not public_key.startswith("mldsa_pk_") or not signature.startswith("mldsa_sig_"):
                return {
                    "ok": False,
                    "raw_reason": "invalid_placeholder_shape",
                    "details": {
                        "public_key_prefix_required": "mldsa_pk_",
                        "signature_prefix_required": "mldsa_sig_",
                    },
                }

            if "fail" in signature:
                return {
                    "ok": False,
                    "raw_reason": "signature_invalid",
                    "details": {"note": "deterministic-signature-failure"},
                }

            return {
                "ok": True,
                "raw_reason": "ok",
                "details": {"note": "deterministic-backend-success"},
            }
        except Exception as exc:
            return sanitize_backend_exception(exc)
