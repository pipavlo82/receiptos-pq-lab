from pathlib import Path

from src.mldsa_fixture_loader import (
    load_mldsa_vector_001,
    to_mldsa_adapter_payload,
    validate_mldsa_fixture_shape,
)
from src.pq_signature_adapter import verify_pq_signature_contract, MLDSAAdapterStub


def test_fixture_file_exists():
    fp = Path(__file__).resolve().parents[1] / "fixtures" / "mldsa" / "vector_001.json"
    assert fp.exists()


def test_fixture_load_and_shape_validation():
    data = load_mldsa_vector_001()
    out = validate_mldsa_fixture_shape(data)
    assert out["valid"] is True
    assert out["missing"] == []


def test_fixture_normalizes_to_adapter_payload():
    data = load_mldsa_vector_001()
    payload = to_mldsa_adapter_payload(data)

    assert payload["scheme_id"] == "MLDSA-65"
    assert payload["canonical_digest"].startswith("0x")
    assert payload["public_key"].startswith("0x")
    assert payload["signature"].startswith("0x")


def test_fixture_payload_passes_adapter_contract_shape():
    data = load_mldsa_vector_001()
    payload = to_mldsa_adapter_payload(data)

    # Uses current adapter contract path; no heavy crypto verify assumed.
    out = verify_pq_signature_contract(payload, MLDSAAdapterStub())

    assert set(out.keys()) == {
        "valid",
        "adapter_result",
        "adapter_reason",
        "normalized_reason_code",
        "details",
    }
    # At this stage we assert integration-shape compatibility, not cryptographic truth.
    assert out["normalized_reason_code"] in {"OK", "VERIFY_FAILED", "ADAPTER_INVALID_INPUT", "ADAPTER_INTERNAL_ERROR"}
