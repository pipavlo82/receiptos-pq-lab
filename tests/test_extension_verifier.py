from __future__ import annotations

import json
from pathlib import Path

from src.extension_verifier import verify_extension


def _examples():
    fp = Path(__file__).resolve().parents[1] / 'examples' / 'extension_payload.sample.json'
    doc = json.loads(fp.read_text(encoding='utf-8'))
    return doc['examples']


def test_auto_detect_signature_mode_valid():
    ex = _examples()[0]
    res = verify_extension({'receipt_extension': ex['receipt_extension']})
    assert res['valid'] is True
    assert res['mode'] == 'signature_extension'
    assert res['reason_code'] == 'OK'


def test_auto_detect_entropy_mode_valid():
    ex = _examples()[1]
    res = verify_extension({'receipt_extension': ex['receipt_extension']})
    assert res['valid'] is True
    assert res['mode'] == 'entropy_proof'
    assert res['reason_code'] == 'OK'


def test_auto_detect_hybrid_mode_valid():
    ex = _examples()[2]
    res = verify_extension({'receipt_extension': ex['receipt_extension']})
    assert res['valid'] is True
    assert res['mode'] == 'hybrid'
    assert res['reason_code'] == 'OK'


def test_missing_required_field_invalid():
    ex = _examples()[0]['receipt_extension']
    bad = json.loads(json.dumps(ex))
    del bad['pq_signature']
    res = verify_extension({'receipt_extension': bad})
    assert res['valid'] is False
    assert res['reason_code'] in {'MISSING_REQUIRED_FIELD', 'MODE_FIELD_MISMATCH'}


def test_wrong_mode_field_mismatch():
    ex = _examples()[1]['receipt_extension']
    bad = json.loads(json.dumps(ex))
    bad['mode'] = 'signature_extension'
    res = verify_extension({'receipt_extension': bad})
    assert res['valid'] is False
    assert res['reason_code'] in {'MODE_FIELD_MISMATCH', 'MISSING_REQUIRED_FIELD'}


def test_hybrid_partial_failure():
    ex = _examples()[2]['receipt_extension']
    bad = json.loads(json.dumps(ex))
    bad['pq_signature']['sig'] = 'bad-sig-demo'
    res = verify_extension({'receipt_extension': bad})
    assert res['valid'] is False
    assert res['reason_code'] == 'HYBRID_PARTIAL_FAILURE'
    assert isinstance(res['fail_path'], dict)
