# Demo Screen Guide (What to show)

## 1) Match Integrity (primary)
- File: `examples/gaming/demo_match_integrity/valid_match_result_receipt.json`
- Then: `tampered_match_result_receipt.json`
- Then: `invalid_continuity_match_result_receipt.json`
- CLI: `python3 scripts/demo_match_integrity.py`

## 2) PQ payload pairing
- Technical fixture: `fixtures/mldsa/vector_001.json`
- Historical payload: `fixtures/mldsa/vector_raw.json`
- Narrative: deterministic engineering path + richer provenance context

## 3) Optional Ethereum anchor
- Contract demo: `ReceiptAnchor` / `GameEventAnchor`
- Show duplicate rejection + continuity guard behavior

## 4) One-slide message
- "Off-chain events become verifiable receipts with deterministic failure semantics; optional on-chain anchoring adds integrity checkpoints."
