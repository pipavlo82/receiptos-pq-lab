import json
from pathlib import Path

from src.stealth_handoff_adapter import adapt_stealth_handoff_evidence


ROOT = Path(__file__).resolve().parents[1]


def load_sample():
    return json.loads((ROOT / 'examples' / 'stealth' / 'session-evidence.v0.sample.json').read_text(encoding='utf-8'))


def load_expected_ok():
    return json.loads((ROOT / 'examples' / 'stealth' / 'adapter-output.ok.v0.json').read_text(encoding='utf-8'))


def test_stealth_adapter_ok():
    evidence = load_sample()
    res = adapt_stealth_handoff_evidence(evidence)
    assert res['valid'] is True
    assert res['reason_code'] == 'OK'
    assert res['fail_path'] is None
    assert res['receiptHash'] == res['receipt']['receiptHash']
    assert res['eventRoot'] == res['receipt']['eventRoot']
    assert isinstance(res['details']['transcript'], list)


def test_stealth_adapter_output_shape_is_stable():
    evidence = load_sample()
    expected = load_expected_ok()
    res = adapt_stealth_handoff_evidence(evidence)
    assert set(res.keys()) == {
        'valid',
        'reason_code',
        'checks',
        'fail_path',
        'details',
        'receipt',
        'receiptHash',
        'eventRoot',
    }
    assert res == expected


def test_stealth_adapter_missing_field_maps_to_tamper():
    evidence = load_sample()
    del evidence['session_id']
    res = adapt_stealth_handoff_evidence(evidence)
    assert res['valid'] is False
    assert res['reason_code'] == 'TAMPER'
    assert res['fail_path'] == 'session_id'
    assert res['receipt'] is None
    assert res['receiptHash'] is None
    assert res['eventRoot'] is None


def test_stealth_adapter_bad_seq_maps_to_chain_mismatch():
    evidence = load_sample()
    evidence['commands'][0]['seq'] = 99
    res = adapt_stealth_handoff_evidence(evidence)
    assert res['valid'] is False
    assert res['reason_code'] == 'CHAIN_MISMATCH'
    assert res['fail_path'] == 'commands'
