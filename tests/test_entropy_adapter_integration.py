from src.entropy_adapter import EntropyAdapter, verify_entropy_contract, verify_entropy_proof_with_adapter
from src.vrf_backend_mock import MockVRFBackend


def _ext(proof: str = "vrf_proof_ok", pub: str = "vrf_pk_ok", score: float = 0.7):
    return {
        "mode": "entropy_proof",
        "entropy": {
            "entropy_score": score,
            "entropy_source": "runtime",
            "freshness_window_sec": 120,
        },
        "vrf": {
            "proof": proof,
            "public_key": pub,
            "domain": "receiptos-pq-lab",
        },
    }


def test_entropy_adapter_contract_success():
    adapter = EntropyAdapter(MockVRFBackend())
    out = verify_entropy_contract(_ext(), adapter)
    assert out["valid"] is True
    assert out["normalized_reason_code"] == "OK"


def test_entropy_adapter_contract_backend_unavailable():
    adapter = EntropyAdapter(MockVRFBackend())
    ext = _ext()
    ext["policy_path"] = {"simulate": "backend_unavailable"}
    out = verify_entropy_contract(ext, adapter)
    assert out["valid"] is False
    assert out["normalized_reason_code"] == "ADAPTER_INTERNAL_ERROR"


def test_entropy_compat_wrapper_stable_shape():
    adapter = EntropyAdapter(MockVRFBackend())
    out = verify_entropy_proof_with_adapter(_ext(proof="vrf_proof_invalid_case"), adapter)
    assert set(["valid", "mode", "reason_code", "checks", "fail_path"]).issubset(out.keys())
    assert set(["adapter_result", "adapter_reason", "normalized_reason_code", "details"]).issubset(out.keys())
    assert out["reason_code"] == "VERIFY_FAILED"
