from __future__ import annotations

from typing import Any, Dict, Protocol

from .reason_mapping import normalize_adapter_output, normalize_exception, normalize_result
from .vrf_backend_interface import VRFBackend, sanitize_backend_exception
from .vrf_backend_mock import MockVRFBackend


class EntropyAdapterContract(Protocol):
    def verify(self, extension: Dict[str, Any]) -> Dict[str, Any]: ...


class EntropyAdapter:
    """Backend-ready entropy adapter preserving stable output contracts."""

    REQUIRED = ("entropy_score", "entropy_source", "freshness_window_sec")

    def __init__(self, backend: VRFBackend | None = None) -> None:
        self.backend = backend or MockVRFBackend()

    def verify(self, extension: Dict[str, Any]) -> Dict[str, Any]:
        if extension.get("mode") not in {"entropy_proof", "hybrid"}:
            return {
                "ok": False,
                "raw_reason": "mode_field_mismatch",
                "details": {"mode": extension.get("mode")},
                "fail_path": "receipt_extension.mode",
            }

        ent = extension.get("entropy")
        if not isinstance(ent, dict):
            return {
                "ok": False,
                "raw_reason": "missing_required_field",
                "details": {"field": "entropy"},
                "fail_path": "receipt_extension.entropy",
            }

        missing = [f for f in self.REQUIRED if ent.get(f) is None or ent.get(f) == ""]
        if missing:
            return {
                "ok": False,
                "raw_reason": "missing_required_field",
                "details": {"missing": missing},
                "fail_path": "receipt_extension.entropy",
            }

        try:
            score = float(ent.get("entropy_score"))
            freshness = int(ent.get("freshness_window_sec"))
        except Exception:
            return {
                "ok": False,
                "raw_reason": "invalid_input",
                "details": {"entropy": ent},
                "fail_path": "receipt_extension.entropy",
            }

        if not (0.0 <= score <= 1.0) or freshness <= 0:
            return {
                "ok": False,
                "raw_reason": "entropy_invalid",
                "details": {"entropy_score": score, "freshness_window_sec": freshness},
                "fail_path": "receipt_extension.entropy",
            }

        vrf_payload = extension.get("vrf") or {}
        metadata = {
            "mode": extension.get("mode"),
            "entropy_source": ent.get("entropy_source"),
        }
        metadata.update((extension.get("policy_path") or {}))

        try:
            backend_raw = self.backend.verify(vrf_payload, metadata)
        except Exception as exc:
            backend_raw = sanitize_backend_exception(exc)

        reason = backend_raw.get("raw_reason") or "internal_error"
        fail_path_map = {
            "missing_required_field": "receipt_extension.vrf",
            "invalid_input": "receipt_extension.vrf",
            "unsupported_proof_shape": "receipt_extension.vrf.proof",
            "invalid_proof": "receipt_extension.vrf.proof",
            "adapter_unavailable": "receipt_extension.vrf",
            "internal_error": "receipt_extension.vrf",
        }

        out = {
            "ok": bool(backend_raw.get("ok")),
            "raw_reason": reason,
            "details": {
                "entropy_score": score,
                "freshness_window_sec": freshness,
                "backend": backend_raw.get("details", {}),
            },
            "fail_path": None if backend_raw.get("ok") else fail_path_map.get(reason),
        }
        return out


# Backward-compatible name for existing callers.
MockEntropyProofAdapter = EntropyAdapter


def verify_entropy_contract(extension: Dict[str, Any], adapter: EntropyAdapterContract) -> Dict[str, Any]:
    try:
        raw = adapter.verify(extension)
        return normalize_adapter_output(raw)
    except Exception as exc:
        base = normalize_exception("entropy_proof", exc, "receipt_extension.entropy")
        return {
            "valid": False,
            "adapter_result": "fail",
            "adapter_reason": "internal_error",
            "normalized_reason_code": base["reason_code"],
            "details": base["checks"]["details"],
        }


def verify_entropy_proof_with_adapter(extension: Dict[str, Any], adapter: EntropyAdapterContract) -> Dict[str, Any]:
    try:
        raw = adapter.verify(extension)
        unified = normalize_result("entropy_proof", raw)
        contract_out = normalize_adapter_output(raw)
        unified.update(contract_out)
        return unified
    except Exception as exc:
        unified = normalize_exception("entropy_proof", exc, "receipt_extension.entropy")
        unified.update(
            {
                "adapter_result": "fail",
                "adapter_reason": "internal_error",
                "normalized_reason_code": unified["reason_code"],
                "details": unified["checks"]["details"],
            }
        )
        return unified
