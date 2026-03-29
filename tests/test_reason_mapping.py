from src.reason_mapping import map_raw_reason, normalize_adapter_output, normalize_result


def test_raw_reason_mapping_levels():
    assert map_raw_reason("ok") == "OK"
    assert map_raw_reason("signature_invalid") == "VERIFY_FAILED"
    assert map_raw_reason("unsupported_scheme") == "ADAPTER_UNSUPPORTED_SCHEME"
    assert map_raw_reason("hybrid_partial_failure") == "HYBRID_PARTIAL_FAILURE"


def test_unknown_reason_falls_back_deterministically():
    assert map_raw_reason("something_new") == "ADAPTER_INTERNAL_ERROR"


def test_normalize_adapter_output_shape():
    out = normalize_adapter_output(
        {
            "ok": False,
            "raw_reason": "missing_required_field",
            "details": {"missing": ["signature"]},
        }
    )
    assert set(out.keys()) == {
        "valid",
        "adapter_result",
        "adapter_reason",
        "normalized_reason_code",
        "details",
    }
    assert out["normalized_reason_code"] == "MISSING_REQUIRED_FIELD"


def test_legacy_normalize_result_shape_unchanged():
    res = normalize_result(
        "signature_extension",
        {
            "ok": False,
            "raw_reason": "missing_required_field",
            "details": {"missing": ["sig"]},
            "fail_path": "receipt_extension.pq_signature",
        },
    )
    assert set(res.keys()) == {"valid", "mode", "reason_code", "checks", "fail_path"}
    assert res["mode"] == "signature_extension"
    assert res["reason_code"] == "MISSING_REQUIRED_FIELD"
