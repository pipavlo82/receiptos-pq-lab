from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict

from .mldsa_fixture_loader import load_mldsa_vector_001
from .mldsa_backend_interface import sanitize_backend_exception


class RealMLDSABackendTransitional:
    """
    Transitional real-backend wrapper.

    Uses local vendor ML-DSA verifier test path (forge) for vector_001 digest flow.
    This does not change adapter/output shape.
    """

    def __init__(self, vendor_repo: str | Path | None = None) -> None:
        if vendor_repo:
            self.vendor_repo = Path(vendor_repo)
        else:
            linux_candidate = Path("/mnt/c/Users/msi/gas-per-secure-bit/vendors/ml-dsa-65-ethereum-verification")
            win_candidate = Path("C:/Users/msi/gas-per-secure-bit/vendors/ml-dsa-65-ethereum-verification")
            self.vendor_repo = linux_candidate if linux_candidate.exists() else win_candidate

    @staticmethod
    def _resolve_forge() -> str | None:
        forge = shutil.which("forge")
        if forge:
            return forge
        candidate = Path.home() / ".foundry" / "bin" / "forge"
        if candidate.exists():
            return str(candidate)
        return None

    def verify(
        self,
        canonical_payload_or_digest: Any,
        public_key: str,
        signature: str,
        metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        try:
            fixture = load_mldsa_vector_001()

            if not isinstance(canonical_payload_or_digest, str):
                return {
                    "ok": False,
                    "raw_reason": "invalid_input",
                    "details": {"field": "canonical_payload_or_digest"},
                }

            # This transitional path is fixture-backed by design (vector_001 only).
            if (
                canonical_payload_or_digest != fixture.get("msg_hash")
                or public_key != fixture.get("public_key_raw")
                or signature != fixture.get("signature_raw")
            ):
                return {
                    "ok": False,
                    "raw_reason": "verify_failed",
                    "details": {"reason": "fixture_mismatch_vector_001"},
                }

            forge = self._resolve_forge()
            if not forge:
                return {
                    "ok": False,
                    "raw_reason": "adapter_unavailable",
                    "details": {"reason": "forge_not_found"},
                }

            cmd = [
                forge,
                "test",
                "--match-test",
                "test_verify_fips_kat_vector0",
                "-vv",
            ]
            proc = subprocess.run(
                cmd,
                cwd=str(self.vendor_repo),
                capture_output=True,
                text=True,
                timeout=240,
                check=False,
            )
            out = (proc.stdout or "") + "\n" + (proc.stderr or "")

            if proc.returncode != 0:
                return {
                    "ok": False,
                    "raw_reason": "adapter_unavailable",
                    "details": {
                        "reason": "forge_test_failed",
                        "returncode": proc.returncode,
                    },
                }

            m = re.search(r"verify_fips_kat_vector0_ok_flag:\s*(\d+)", out)
            ok_flag = int(m.group(1)) if m else -1

            if ok_flag == 1:
                return {
                    "ok": True,
                    "raw_reason": "ok",
                    "details": {
                        "backend": "forge_mldsa65_verifier",
                        "ok_flag": ok_flag,
                        "mode": "real_transitional",
                    },
                }

            return {
                "ok": False,
                "raw_reason": "verify_failed",
                "details": {
                    "backend": "forge_mldsa65_verifier",
                    "ok_flag": ok_flag,
                    "mode": "real_transitional",
                },
            }
        except Exception as exc:
            return sanitize_backend_exception(exc)
