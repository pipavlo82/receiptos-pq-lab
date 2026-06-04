import json
from pathlib import Path

from src.stealth_handoff_adapter import adapt_stealth_handoff_evidence, verify_trust_block


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
    assert res['trust'] == res['receipt']['trust']
    assert isinstance(res['details']['transcript'], list)


def test_stealth_adapter_transcript_is_sequence_aware():
    evidence = load_sample()
    res = adapt_stealth_handoff_evidence(evidence)
    transcript = res['details']['transcript']
    assert [event['seq'] for event in transcript] == [1, 2]
    assert transcript[0]['type'] == 'command'
    assert transcript[1]['type'] == 'change'
    assert transcript[0]['prev_hash'] == 'GENESIS'
    assert transcript[1]['prev_hash'] == transcript[0]['event_hash']
    assert res['eventRoot'] == transcript[-1]['event_hash']


def test_stealth_adapter_event_hash_changes_with_command_content():
    evidence = load_sample()
    original = adapt_stealth_handoff_evidence(evidence)
    evidence['commands'][0]['stdout_summary'] = 'changed-output-summary'
    changed = adapt_stealth_handoff_evidence(evidence)
    assert original['details']['transcript'][0]['event_hash'] != changed['details']['transcript'][0]['event_hash']
    assert original['eventRoot'] != changed['eventRoot']


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
        'trust',
    }
    assert res == expected


def test_stealth_adapter_missing_field_maps_to_missing_required_field():
    evidence = load_sample()
    del evidence['session_id']
    res = adapt_stealth_handoff_evidence(evidence)
    assert res['valid'] is False
    assert res['reason_code'] == 'MISSING_REQUIRED_FIELD'
    assert res['fail_path'] == 'session_id'
    assert res['receipt'] is None
    assert res['receiptHash'] is None
    assert res['eventRoot'] is None
    assert res['trust'] is None


def test_stealth_adapter_bad_schema_maps_cleanly():
    evidence = load_sample()
    evidence['schema'] = 'wrong.schema.v0'
    res = adapt_stealth_handoff_evidence(evidence)
    assert res['valid'] is False
    assert res['reason_code'] == 'BAD_SCHEMA'
    assert res['fail_path'] == 'schema'


def test_stealth_adapter_empty_transcript_maps_cleanly():
    evidence = load_sample()
    evidence['commands'] = []
    evidence['changes'] = {'files_changed': [], 'diff_sha256': None}
    evidence['metadata']['diff_count'] = 0
    res = adapt_stealth_handoff_evidence(evidence)
    assert res['valid'] is False
    assert res['reason_code'] == 'EMPTY_TRANSCRIPT'
    assert res['fail_path'] == 'commands'


def test_stealth_adapter_diff_mismatch_maps_cleanly():
    evidence = load_sample()
    evidence['changes'] = {'files_changed': ['README.md'], 'diff_sha256': None}
    res = adapt_stealth_handoff_evidence(evidence)
    assert res['valid'] is False
    assert res['reason_code'] == 'DIFF_MISMATCH'
    assert res['fail_path'] == 'changes.diff_sha256'


def test_stealth_adapter_tamper_maps_cleanly():
    evidence = load_sample()
    evidence['commands'][0]['command'] = ''
    res = adapt_stealth_handoff_evidence(evidence)
    assert res['valid'] is False
    assert res['reason_code'] == 'TAMPER'
    assert res['fail_path'] == 'commands[0].command'


def test_stealth_adapter_bad_seq_maps_to_chain_mismatch():
    evidence = load_sample()
    evidence['commands'][0]['seq'] = 99
    res = adapt_stealth_handoff_evidence(evidence)
    assert res['valid'] is False
    assert res['reason_code'] == 'CHAIN_MISMATCH'
    assert res['fail_path'] == 'commands'


def test_trust_block_missing_signature_maps_cleanly():
    evidence = load_sample()
    res = adapt_stealth_handoff_evidence(evidence)
    trust = dict(res['trust'])
    del trust['signature']
    ok, reason, fail_path, checks = verify_trust_block(res['receiptHash'], res['eventRoot'], trust)
    assert ok is False
    assert reason == 'MISSING_SIGNATURE'
    assert fail_path == 'trust.signature'


def test_trust_block_bad_signature_maps_cleanly():
    evidence = load_sample()
    res = adapt_stealth_handoff_evidence(evidence)
    trust = dict(res['trust'])
    trust['signature'] = 'bad-signature'
    ok, reason, fail_path, checks = verify_trust_block(res['receiptHash'], res['eventRoot'], trust)
    assert ok is False
    assert reason == 'BAD_SIGNATURE'
    assert fail_path == 'trust.signature'


def test_trust_block_wrong_signed_fields_maps_cleanly():
    evidence = load_sample()
    res = adapt_stealth_handoff_evidence(evidence)
    trust = dict(res['trust'])
    trust['signed_fields'] = ['receiptHash']
    ok, reason, fail_path, checks = verify_trust_block(res['receiptHash'], res['eventRoot'], trust)
    assert ok is False
    assert reason == 'TRUST_BLOCK_INVALID'
    assert fail_path == 'trust.signed_fields'


def test_trust_block_receipt_hash_mismatch_maps_bad_signature():
    evidence = load_sample()
    res = adapt_stealth_handoff_evidence(evidence)
    ok, reason, fail_path, checks = verify_trust_block('wrong-hash', res['eventRoot'], dict(res['trust']))
    assert ok is False
    assert reason == 'BAD_SIGNATURE'
    assert fail_path == 'trust.signature'


def test_trust_block_event_root_mismatch_maps_bad_signature():
    evidence = load_sample()
    res = adapt_stealth_handoff_evidence(evidence)
    ok, reason, fail_path, checks = verify_trust_block(res['receiptHash'], 'wrong-root', dict(res['trust']))
    assert ok is False
    assert reason == 'BAD_SIGNATURE'
    assert fail_path == 'trust.signature'


def test_stealth_adapter_internal_error_maps_cleanly(monkeypatch):
    import src.stealth_handoff_adapter as adapter

    def boom(_obj):
        raise RuntimeError('boom')

    monkeypatch.setattr(adapter, 'sha256_hex_obj', boom)
    evidence = load_sample()
    res = adapter.adapt_stealth_handoff_evidence(evidence)
    assert res['valid'] is False
    assert res['reason_code'] == 'ADAPTER_INTERNAL_ERROR'
    assert res['fail_path'] is None
