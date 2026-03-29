from src.mldsa_backend_mock import MockMLDSABackend


def test_backend_mock_success():
    b = MockMLDSABackend()
    out = b.verify("sha256:abc", "mldsa_pk_demo", "mldsa_sig_ok", {})
    assert out["ok"] is True
    assert out["raw_reason"] == "ok"


def test_backend_mock_signature_invalid():
    b = MockMLDSABackend()
    out = b.verify("sha256:abc", "mldsa_pk_demo", "mldsa_sig_fail_case", {})
    assert out["ok"] is False
    assert out["raw_reason"] == "signature_invalid"


def test_backend_mock_invalid_shape():
    b = MockMLDSABackend()
    out = b.verify("sha256:abc", "pk_demo", "sig_demo", {})
    assert out["ok"] is False
    assert out["raw_reason"] == "invalid_placeholder_shape"


def test_backend_mock_unavailable():
    b = MockMLDSABackend()
    out = b.verify("sha256:abc", "mldsa_pk_demo", "mldsa_sig_ok", {"simulate": "backend_unavailable"})
    assert out["ok"] is False
    assert out["raw_reason"] == "adapter_unavailable"


def test_backend_mock_internal_failure():
    b = MockMLDSABackend()
    out = b.verify("sha256:abc", "mldsa_pk_demo", "mldsa_sig_ok", {"simulate": "internal_failure"})
    assert out["ok"] is False
    assert out["raw_reason"] == "internal_error"
