from src.vrf_backend_mock import MockVRFBackend


def test_vrf_backend_success():
    b = MockVRFBackend()
    out = b.verify({"proof": "vrf_proof_ok", "public_key": "vrf_pk_ok"}, {})
    assert out["ok"] is True
    assert out["raw_reason"] == "ok"


def test_vrf_backend_invalid_proof():
    b = MockVRFBackend()
    out = b.verify({"proof": "vrf_proof_invalid_case", "public_key": "vrf_pk_ok"}, {})
    assert out["ok"] is False
    assert out["raw_reason"] == "invalid_proof"


def test_vrf_backend_unsupported_shape():
    b = MockVRFBackend()
    out = b.verify({"proof": "proof", "public_key": "pk"}, {})
    assert out["ok"] is False
    assert out["raw_reason"] == "unsupported_proof_shape"


def test_vrf_backend_unavailable():
    b = MockVRFBackend()
    out = b.verify({"proof": "vrf_proof_ok", "public_key": "vrf_pk_ok"}, {"simulate": "backend_unavailable"})
    assert out["ok"] is False
    assert out["raw_reason"] == "adapter_unavailable"


def test_vrf_backend_internal_failure():
    b = MockVRFBackend()
    out = b.verify({"proof": "vrf_proof_ok", "public_key": "vrf_pk_ok"}, {"simulate": "internal_failure"})
    assert out["ok"] is False
    assert out["raw_reason"] == "internal_error"
