from __future__ import annotations

from src.mock_signature_extension import verify_signature_extension
from src.mock_entropy_proof import verify_entropy_proof
from src.mock_hybrid import verify_hybrid


def test_mock_signature_valid():
    ext = {
        'extension_version': 'x1',
        'mode': 'signature_extension',
        'pq_signature': {'alg': 'PQ-ALG', 'key_id': 'pq-k1', 'sig': 'sig-ok'}
    }
    res = verify_signature_extension(ext)
    assert res['valid'] is True
    assert res['reason_code'] == 'OK'


def test_mock_signature_invalid_sig():
    ext = {
        'extension_version': 'x1',
        'mode': 'signature_extension',
        'pq_signature': {'alg': 'PQ-ALG', 'key_id': 'pq-k1', 'sig': 'bad-signature'}
    }
    res = verify_signature_extension(ext)
    assert res['valid'] is False
    assert res['reason_code'] == 'MOCK_SIGNATURE_INVALID'


def test_mock_entropy_valid():
    ext = {
        'extension_version': 'x1',
        'mode': 'entropy_proof',
        'entropy': {'entropy_score': 0.7, 'entropy_source': 'runtime', 'freshness_window_sec': 120}
    }
    res = verify_entropy_proof(ext)
    assert res['valid'] is True
    assert res['reason_code'] == 'OK'


def test_mock_entropy_invalid_score():
    ext = {
        'extension_version': 'x1',
        'mode': 'entropy_proof',
        'entropy': {'entropy_score': 1.5, 'entropy_source': 'runtime', 'freshness_window_sec': 120}
    }
    res = verify_entropy_proof(ext)
    assert res['valid'] is False
    assert res['reason_code'] == 'MOCK_ENTROPY_INVALID'


def test_mock_hybrid_partial_failure():
    ext = {
        'extension_version': 'x1',
        'mode': 'hybrid',
        'pq_signature': {'alg': 'PQ-ALG', 'key_id': 'pq-k1', 'sig': 'sig-ok'},
        'entropy': {'entropy_score': -0.1, 'entropy_source': 'runtime', 'freshness_window_sec': 120}
    }
    res = verify_hybrid(ext)
    assert res['valid'] is False
    assert res['reason_code'] == 'HYBRID_PARTIAL_FAILURE'
