from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any, Dict


DEFAULT_HISTORICAL_FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "mldsa" / "vector_raw.json"
REQUIRED_FIELDS = ("msg_hash", "sig_pq_b64", "pq_pubkey_b64")


def load_mldsa_vector_raw(path: str | Path | None = None) -> Dict[str, Any]:
    fp = Path(path) if path else DEFAULT_HISTORICAL_FIXTURE
    return json.loads(fp.read_text(encoding="utf-8"))


def decode_vector_raw_fields(data: Dict[str, Any]) -> Dict[str, Any]:
    missing = [k for k in REQUIRED_FIELDS if not data.get(k)]
    if missing:
        return {"valid": False, "missing": missing}

    sig_bytes = base64.b64decode(data["sig_pq_b64"])
    pk_bytes = base64.b64decode(data["pq_pubkey_b64"])

    metadata = {
        k: v
        for k, v in data.items()
        if k not in {"sig_pq_b64", "pq_pubkey_b64", "msg_hash"}
    }

    return {
        "valid": True,
        "missing": [],
        "msg_hash": data["msg_hash"],
        "signature_bytes": sig_bytes,
        "public_key_bytes": pk_bytes,
        "signature_hex": "0x" + sig_bytes.hex(),
        "public_key_hex": "0x" + pk_bytes.hex(),
        "metadata": metadata,
    }


def to_mldsa_adapter_payload_from_vector_raw(data: Dict[str, Any]) -> Dict[str, Any]:
    dec = decode_vector_raw_fields(data)
    if not dec.get("valid"):
        raise ValueError(f"invalid vector_raw fixture: missing={dec.get('missing')}")

    md = dict(dec["metadata"])
    md.update(
        {
            "fixture": "vector_raw",
            "source": "test_vectors/vector_raw.json",
            "flow": "verify-by-digest",
        }
    )

    return {
        "scheme_id": "MLDSA-65",
        "canonical_digest": dec["msg_hash"],
        "public_key": dec["public_key_hex"],
        "signature": dec["signature_hex"],
        "metadata": md,
    }
