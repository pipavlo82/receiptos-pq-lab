from pathlib import Path

from src.mldsa_historical_loader import (
    load_mldsa_vector_raw,
    decode_vector_raw_fields,
    to_mldsa_adapter_payload_from_vector_raw,
)


def test_vector_raw_fixture_exists():
    fp = Path(__file__).resolve().parents[1] / "fixtures" / "mldsa" / "vector_raw.json"
    assert fp.exists()


def test_vector_raw_load_and_decode():
    data = load_mldsa_vector_raw()
    dec = decode_vector_raw_fields(data)

    assert dec["valid"] is True
    assert dec["msg_hash"].startswith("0x")
    assert dec["signature_hex"].startswith("0x")
    assert dec["public_key_hex"].startswith("0x")
    assert len(dec["signature_bytes"]) > 0
    assert len(dec["public_key_bytes"]) > 0


def test_vector_raw_maps_to_adapter_payload_and_keeps_metadata():
    data = load_mldsa_vector_raw()
    payload = to_mldsa_adapter_payload_from_vector_raw(data)

    assert payload["scheme_id"] == "MLDSA-65"
    assert payload["canonical_digest"].startswith("0x")
    assert payload["signature"].startswith("0x")
    assert payload["public_key"].startswith("0x")
    assert payload["metadata"].get("signature_type") is not None
    assert payload["metadata"].get("fixture") == "vector_raw"
