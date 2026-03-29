from src.mldsa_adapter_stub import verify_mldsa_stub


def test_mldsa_stub_valid_digest_path():
    payload = {
        "scheme_id": "MLDSA-STUB-V1",
        "canonical_digest": "sha256:abc",
        "public_key": "mldsa_pk_demo",
        "signature": "mldsa_sig_demo",
    }
    res = verify_mldsa_stub(payload)
    assert res["ok"] is True
    assert res["raw_reason"] == "ok"


def test_mldsa_stub_missing_required_fields():
    res = verify_mldsa_stub({"scheme_id": "MLDSA-STUB-V1"})
    assert res["ok"] is False
    assert res["raw_reason"] == "missing_required_field"


def test_mldsa_stub_unsupported_scheme():
    payload = {
        "scheme_id": "UNKNOWN-SCHEME",
        "canonical_digest": "sha256:abc",
        "public_key": "mldsa_pk_demo",
        "signature": "mldsa_sig_demo",
    }
    res = verify_mldsa_stub(payload)
    assert res["ok"] is False
    assert res["raw_reason"] == "unsupported_scheme"


def test_mldsa_stub_placeholder_shape_check():
    payload = {
        "scheme_id": "MLDSA-STUB-V1",
        "canonical_digest": "sha256:abc",
        "public_key": "pk_demo",
        "signature": "sig_demo",
    }
    res = verify_mldsa_stub(payload)
    assert res["ok"] is False
    assert res["raw_reason"] == "invalid_placeholder_shape"


def test_mldsa_stub_deterministic_signature_failure():
    payload = {
        "scheme_id": "MLDSA-STUB-V1",
        "canonical_digest": "sha256:abc",
        "public_key": "mldsa_pk_demo",
        "signature": "mldsa_sig_fail_case",
    }
    res = verify_mldsa_stub(payload)
    assert res["ok"] is False
    assert res["raw_reason"] == "signature_invalid"
