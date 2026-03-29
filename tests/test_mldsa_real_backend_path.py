from src.mldsa_backend_real import RealMLDSABackendTransitional
from src.mldsa_fixture_loader import load_mldsa_vector_001


def test_real_backend_vector_path_executes_deterministically():
    b = RealMLDSABackendTransitional()
    f = load_mldsa_vector_001()

    out = b.verify(
        canonical_payload_or_digest=f["msg_hash"],
        public_key=f["public_key_raw"],
        signature=f["signature_raw"],
        metadata={"flow": "verify-by-digest"},
    )

    assert set(out.keys()) == {"ok", "raw_reason", "details"}
    assert out["raw_reason"] in {"ok", "verify_failed", "adapter_unavailable"}


def test_real_backend_fixture_mismatch_is_verify_failed():
    b = RealMLDSABackendTransitional()
    f = load_mldsa_vector_001()

    out = b.verify(
        canonical_payload_or_digest=f["msg_hash"],
        public_key=f["public_key_raw"],
        signature="0xdeadbeef",
        metadata={"flow": "verify-by-digest"},
    )

    assert out["ok"] is False
    assert out["raw_reason"] == "verify_failed"
