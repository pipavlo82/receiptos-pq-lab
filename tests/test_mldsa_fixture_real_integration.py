from src.mldsa_adapter import MLDSAAdapter
from src.mldsa_backend_real import RealMLDSABackendTransitional
from src.mldsa_fixture_loader import load_mldsa_vector_001, to_mldsa_adapter_payload
from src.pq_signature_adapter import verify_pq_signature_contract


def test_fixture_through_real_backend_keeps_output_shape():
    fixture = load_mldsa_vector_001()
    payload = to_mldsa_adapter_payload(fixture)

    adapter = MLDSAAdapter(RealMLDSABackendTransitional())
    out = verify_pq_signature_contract(payload, adapter)

    assert set(out.keys()) == {
        "valid",
        "adapter_result",
        "adapter_reason",
        "normalized_reason_code",
        "details",
    }
    assert out["normalized_reason_code"] in {"OK", "VERIFY_FAILED", "ADAPTER_INTERNAL_ERROR"}


def test_fixture_real_backend_mismatch_maps_to_verify_failed():
    fixture = load_mldsa_vector_001()
    payload = to_mldsa_adapter_payload(fixture)
    payload["signature"] = "0xdeadbeef"

    adapter = MLDSAAdapter(RealMLDSABackendTransitional())
    out = verify_pq_signature_contract(payload, adapter)

    assert out["valid"] is False
    assert out["normalized_reason_code"] == "VERIFY_FAILED"
