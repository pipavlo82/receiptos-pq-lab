import json
from pathlib import Path

from src.stealth_handoff_adapter import adapt_stealth_handoff_evidence


def load_sample():
    root = Path(__file__).resolve().parents[1]
    return json.loads((root / 'examples' / 'stealth' / 'session-evidence.v0.sample.json').read_text(encoding='utf-8'))


def test_stealth_adapter_ok():
    evidence = load_sample()
    res = adapt_stealth_handoff_evidence(evidence)
    assert res['valid'] is True
    assert res['reason_code'] == 'OK'
    assert res['fail_path'] is None
    assert 'receiptHash' in res['details']['receipt']
    assert 'eventRoot' in res['details']['receipt']
    assert isinstance(res['details']['transcript'], list)


def test_stealth_adapter_missing_field_maps_to_tamper():
    evidence = load_sample()
    del evidence['session_id']
    res = adapt_stealth_handoff_evidence(evidence)
    assert res['valid'] is False
    assert res['reason_code'] == 'TAMPER'
    assert res['fail_path'] == 'session_id'


def test_stealth_adapter_bad_seq_maps_to_chain_mismatch():
    evidence = load_sample()
    evidence['commands'][0]['seq'] = 99
    res = adapt_stealth_handoff_evidence(evidence)
    assert res['valid'] is False
    assert res['reason_code'] == 'CHAIN_MISMATCH'
    assert res['fail_path'] == 'commands'
