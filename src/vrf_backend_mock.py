from __future__ import annotations

from typing import Any, Dict

from .vrf_backend_interface import sanitize_backend_exception


class MockVRFBackend:
    """Deterministic VRF/entropy backend mock."""

    def verify(self, entropy_proof_payload: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if metadata.get("simulate") == "backend_unavailable":
                return {
                    "ok": False,
                    "raw_reason": "adapter_unavailable",
                    "details": {"source": "mock_vrf_backend"},
                }

            if metadata.get("simulate") == "internal_failure":
                raise RuntimeError("simulated vrf backend failure")

            if not isinstance(entropy_proof_payload, dict):
                return {
                    "ok": False,
                    "raw_reason": "invalid_input",
                    "details": {"field": "entropy_proof_payload"},
                }

            proof = str(entropy_proof_payload.get("proof") or "")
            public_key = str(entropy_proof_payload.get("public_key") or "")

            if not proof or not public_key:
                return {
                    "ok": False,
                    "raw_reason": "missing_required_field",
                    "details": {"missing": [k for k, v in {"proof": proof, "public_key": public_key}.items() if not v]},
                }

            if not proof.startswith("vrf_proof_") or not public_key.startswith("vrf_pk_"):
                return {
                    "ok": False,
                    "raw_reason": "unsupported_proof_shape",
                    "details": {
                        "proof_prefix_required": "vrf_proof_",
                        "public_key_prefix_required": "vrf_pk_",
                    },
                }

            if "invalid" in proof:
                return {
                    "ok": False,
                    "raw_reason": "invalid_proof",
                    "details": {"note": "deterministic-proof-failure"},
                }

            return {
                "ok": True,
                "raw_reason": "ok",
                "details": {"note": "deterministic-vrf-success"},
            }
        except Exception as exc:
            return sanitize_backend_exception(exc)
