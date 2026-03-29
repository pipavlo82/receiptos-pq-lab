from src.pq_signature_adapter import (
    MLDSAAdapterStub,
    verify_pq_signature_contract,
    verify_pq_signature_with_adapter,
)
from src.entropy_proof_adapter import MockEntropyProofAdapter, verify_entropy_proof_with_adapter
from src.hybrid_adapter import verify_hybrid_with_adapters


class BrokenAdapter:
    def verify(self, payload):
        raise RuntimeError("boom")


def test_pq_adapter_contract_valid_output_shape():
    payload = {
        "scheme_id": "MLDSA-STUB-V1",
        "canonical_digest": "sha256:abc",
        "public_key": "mldsa_pk_demo",
        "signature": "mldsa_sig_ok",
        "metadata": {"lane": "demo"},
    }
    res = verify_pq_signature_contract(payload, MLDSAAdapterStub())
    assert set(res.keys()) == {
        "valid",
        "adapter_result",
        "adapter_reason",
        "normalized_reason_code",
        "details",
    }
    assert res["valid"] is True
    assert res["normalized_reason_code"] == "OK"


def test_entropy_adapter_contract_missing_field():
    ext = {
        "mode": "entropy_proof",
        "entropy": {"entropy_score": 0.5, "entropy_source": "runtime"},
    }
    res = verify_entropy_proof_with_adapter(ext, MockEntropyProofAdapter())
    assert res["valid"] is False
    assert res["reason_code"] == "MISSING_REQUIRED_FIELD"


def test_hybrid_partial_failure_normalized():
    ext = {
        "mode": "hybrid",
        "pq_signature": {
            "alg": "MLDSA-STUB-V1",
            "key_id": "k1",
            "sig": "mldsa_sig_ok",
            "public_key": "mldsa_pk_ok",
        },
        "canonical_digest": "sha256:abc",
        "entropy": {"entropy_score": 1.9, "entropy_source": "runtime", "freshness_window_sec": 120},
    }
    res = verify_hybrid_with_adapters(ext, MLDSAAdapterStub(), MockEntropyProofAdapter())
    assert res["valid"] is False
    assert res["reason_code"] == "HYBRID_PARTIAL_FAILURE"
    assert isinstance(res["fail_path"], dict)


def test_adapter_exception_maps_to_deterministic_failure():
    ext = {
        "mode": "signature_extension",
        "pq_signature": {
            "alg": "MLDSA-STUB-V1",
            "key_id": "k1",
            "sig": "mldsa_sig_ok",
            "public_key": "mldsa_pk_ok",
        },
        "canonical_digest": "sha256:abc",
    }
    res = verify_pq_signature_with_adapter(ext, BrokenAdapter())
    assert res["valid"] is False
    assert res["reason_code"] == "ADAPTER_INTERNAL_ERROR"
    assert res["normalized_reason_code"] == "ADAPTER_INTERNAL_ERROR"
