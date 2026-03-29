from __future__ import annotations

from typing import Any, Dict

from .mldsa_backend_interface import MLDSABackend, sanitize_backend_exception
from .mldsa_backend_mock import MockMLDSABackend


class MLDSAAdapter:
    """
    Real-implementation-ready adapter boundary.

    Keeps adapter contract stable while delegating verification mechanics
    to a backend implementing MLDSABackend.
    """

    def __init__(self, backend: MLDSABackend | None = None) -> None:
        self.backend = backend or MockMLDSABackend()

    def verify(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(payload, dict):
            return {
                "ok": False,
                "raw_reason": "invalid_input",
                "details": {"expected": "dict"},
                "fail_path": "payload",
            }

        missing = [k for k in ("scheme_id", "public_key", "signature") if not payload.get(k)]
        if missing:
            return {
                "ok": False,
                "raw_reason": "missing_required_field",
                "details": {"missing": missing},
                "fail_path": "payload",
            }

        canonical = payload.get("canonical_payload")
        digest = payload.get("canonical_digest")
        if not canonical and not digest:
            return {
                "ok": False,
                "raw_reason": "missing_required_field",
                "details": {"missing": ["canonical_payload|canonical_digest"]},
                "fail_path": "payload.canonical_payload",
            }

        scheme = str(payload.get("scheme_id"))
        if not scheme.startswith("MLDSA"):
            return {
                "ok": False,
                "raw_reason": "unsupported_scheme",
                "details": {"scheme_id": scheme, "expected_prefix": "MLDSA"},
                "fail_path": "payload.scheme_id",
            }

        metadata = payload.get("metadata") or {}
        metadata = dict(metadata)
        metadata.setdefault("scheme_id", scheme)

        try:
            backend_raw = self.backend.verify(
                canonical_payload_or_digest=(canonical if canonical else digest),
                public_key=str(payload.get("public_key")),
                signature=str(payload.get("signature")),
                metadata=metadata,
            )
        except Exception as exc:
            backend_raw = sanitize_backend_exception(exc)

        # Keep adapter raw shape stable, attach deterministic fail_path mapping.
        fail_path_map = {
            "missing_required_field": "payload",
            "invalid_input": "payload",
            "unsupported_scheme": "payload.scheme_id",
            "invalid_placeholder_shape": "payload.public_key",
            "signature_invalid": "payload.signature",
            "adapter_unavailable": "payload",
            "internal_error": "payload",
        }

        out = {
            "ok": bool(backend_raw.get("ok")),
            "raw_reason": backend_raw.get("raw_reason") or "internal_error",
            "details": backend_raw.get("details", {}),
            "fail_path": fail_path_map.get(backend_raw.get("raw_reason")),
        }

        if out["ok"]:
            out["fail_path"] = None
        return out
