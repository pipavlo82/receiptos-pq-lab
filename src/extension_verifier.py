from __future__ import annotations

from typing import Any, Dict

from .mock_signature_extension import verify_signature_extension
from .mock_entropy_proof import verify_entropy_proof
from .mock_hybrid import verify_hybrid


SUPPORTED_MODES = {"signature_extension", "entropy_proof", "hybrid"}


def verify_extension(receipt_or_extension: Dict[str, Any]) -> Dict[str, Any]:
    """
    Unified extension verifier output format:
    - valid: bool
    - mode: str|None
    - reason_code: str
    - checks: object
    - fail_path: str|object|None
    """
    if not isinstance(receipt_or_extension, dict):
        return {
            "valid": False,
            "mode": None,
            "reason_code": "INVALID_EXTENSION_SCHEMA",
            "checks": {"type": str(type(receipt_or_extension))},
            "fail_path": "receipt_extension",
        }

    ext = receipt_or_extension.get("receipt_extension") if "receipt_extension" in receipt_or_extension else receipt_or_extension
    if not isinstance(ext, dict):
        return {
            "valid": False,
            "mode": None,
            "reason_code": "INVALID_EXTENSION_SCHEMA",
            "checks": {"receipt_extension_present": False},
            "fail_path": "receipt_extension",
        }

    mode = ext.get("mode")
    version = ext.get("extension_version")
    if version != "x1":
        return {
            "valid": False,
            "mode": mode,
            "reason_code": "INVALID_EXTENSION_SCHEMA",
            "checks": {"extension_version": version, "expected": "x1"},
            "fail_path": "receipt_extension.extension_version",
        }

    if mode not in SUPPORTED_MODES:
        return {
            "valid": False,
            "mode": mode,
            "reason_code": "UNKNOWN_MODE",
            "checks": {"supported_modes": sorted(SUPPORTED_MODES)},
            "fail_path": "receipt_extension.mode",
        }

    if mode == "signature_extension":
        return verify_signature_extension(ext)
    if mode == "entropy_proof":
        return verify_entropy_proof(ext)
    return verify_hybrid(ext)
