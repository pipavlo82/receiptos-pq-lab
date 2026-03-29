from src.mldsa_adapter import MLDSAAdapter
from src.mldsa_backend_mock import MockMLDSABackend
from src.pq_signature_adapter import verify_pq_signature_contract, verify_pq_signature_with_adapter


def _ext(sig: str = "mldsa_sig_ok", pub: str = "mldsa_pk_ok", alg: str = "MLDSA-STUB-V1", meta: dict | None = None):
    ext = {
        "mode": "signature_extension",
        "canonical_digest": "sha256:abc",
        "pq_signature": {
            "alg": alg,
            "key_id": "k1",
            "sig": sig,
            "public_key": pub,
        },
        "policy_path": {"selected_path": "signature_extension"},
    }
    if meta:
        ext["policy_path"].update(meta)
    return ext


def test_adapter_contract_success_path():
    adapter = MLDSAAdapter(MockMLDSABackend())
    payload = {
        "scheme_id": "MLDSA-STUB-V1",
        "canonical_digest": "sha256:abc",
        "public_key": "mldsa_pk_ok",
        "signature": "mldsa_sig_ok",
        "metadata": {},
    }
    res = verify_pq_signature_contract(payload, adapter)
    assert res["valid"] is True
    assert res["normalized_reason_code"] == "OK"


def test_adapter_contract_backend_unavailable():
    adapter = MLDSAAdapter(MockMLDSABackend())
    payload = {
        "scheme_id": "MLDSA-STUB-V1",
        "canonical_digest": "sha256:abc",
        "public_key": "mldsa_pk_ok",
        "signature": "mldsa_sig_ok",
        "metadata": {"simulate": "backend_unavailable"},
    }
    res = verify_pq_signature_contract(payload, adapter)
    assert res["valid"] is False
    assert res["normalized_reason_code"] == "ADAPTER_INTERNAL_ERROR"


def test_compatibility_wrapper_stable_shape():
    adapter = MLDSAAdapter(MockMLDSABackend())
    res = verify_pq_signature_with_adapter(_ext(sig="mldsa_sig_fail_case"), adapter)
    assert set(["valid", "mode", "reason_code", "checks", "fail_path"]).issubset(res.keys())
    assert set(["adapter_result", "adapter_reason", "normalized_reason_code", "details"]).issubset(res.keys())
    assert res["reason_code"] == "VERIFY_FAILED"
