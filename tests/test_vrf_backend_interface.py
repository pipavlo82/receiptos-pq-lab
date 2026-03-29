from src.vrf_backend_interface import sanitize_backend_exception


def test_sanitize_vrf_backend_exception_deterministic():
    out = sanitize_backend_exception(RuntimeError("secret details"))
    assert out["ok"] is False
    assert out["raw_reason"] == "internal_error"
    assert out["details"]["error"] == "backend_internal_error"
    assert "secret" not in out["details"]["error"]
