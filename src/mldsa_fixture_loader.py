from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


DEFAULT_FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "mldsa" / "vector_001.json"


REQUIRED_FIELDS = ("msg_hash", "public_key_raw", "signature_raw")


def load_mldsa_vector_001(path: str | Path | None = None) -> Dict[str, Any]:
    fp = Path(path) if path else DEFAULT_FIXTURE
    data = json.loads(fp.read_text(encoding="utf-8"))
    return data


def validate_mldsa_fixture_shape(data: Dict[str, Any]) -> Dict[str, Any]:
    missing = [k for k in REQUIRED_FIELDS if not data.get(k)]
    if missing:
        return {"valid": False, "missing": missing}

    checks = {
        "msg_hash_is_hex": isinstance(data.get("msg_hash"), str) and data["msg_hash"].startswith("0x"),
        "public_key_raw_is_hex": isinstance(data.get("public_key_raw"), str) and data["public_key_raw"].startswith("0x"),
        "signature_raw_is_hex": isinstance(data.get("signature_raw"), str) and data["signature_raw"].startswith("0x"),
    }
    return {"valid": all(checks.values()), "missing": [], "checks": checks}


def to_mldsa_adapter_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize fixture into current PQ adapter contract payload (verify-by-digest flow).
    """
    return {
        "scheme_id": "MLDSA-65",
        "canonical_digest": data.get("msg_hash"),
        "public_key": data.get("public_key_raw"),
        "signature": data.get("signature_raw"),
        "metadata": {
            "fixture": "vector_001",
            "source": "ml-dsa-65-ethereum-verification/test_vectors/vector_001.json",
            "flow": "verify-by-digest",
        },
    }
