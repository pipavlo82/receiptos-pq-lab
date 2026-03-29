from __future__ import annotations

from typing import Any, Dict, Protocol

from .reason_mapping import normalize_exception, normalize_result


class EntropyProofAdapter(Protocol):
    """
    Contract for entropy-proof adapters.

    input payload shape:
      {
        "mode": "entropy_proof" | "hybrid",
        "entropy": {"entropy_score": number, "entropy_source": str, "freshness_window_sec": int, ...},
        "vrf": {...} (optional)
      }

    verify(...) raw return shape:
      {
        "ok": bool,
        "raw_reason": str,
        "details": dict,
        "fail_path": str|None
      }
    """

    def verify(self, extension: Dict[str, Any]) -> Dict[str, Any]: ...


class MockEntropyProofAdapter:
    REQUIRED = ("entropy_score", "entropy_source", "freshness_window_sec")

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

        return {
            "ok": True,
            "raw_reason": "ok",
            "details": {"entropy_score": score, "freshness_window_sec": freshness},
            "fail_path": None,
        }


def verify_entropy_proof_with_adapter(extension: Dict[str, Any], adapter: EntropyProofAdapter) -> Dict[str, Any]:
    try:
        raw = adapter.verify(extension)
        return normalize_result("entropy_proof", raw)
    except Exception as exc:
        return normalize_exception("entropy_proof", exc, "receipt_extension.entropy")
