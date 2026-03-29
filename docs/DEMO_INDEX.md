# Demo Index

## 1) ReceiptOS MVP Demo (baseline)
- Scope: core verifiable execution semantics
- See: `receiptos-mvp` demo docs/scripts
- Focus: sign/verify/replay/chain baseline

## 2) Gaming Demos (vertical)
- Loot fairness:
  - `docs/GAMING_DEMO_LOOT_FAIRNESS.md`
  - `examples/gaming/demo_loot_fairness/`
- Match integrity:
  - `docs/GAMING_DEMO_MATCH_INTEGRITY.md`
  - `docs/DEMO_MATCH_INTEGRITY_SCRIPT.md`
  - `examples/gaming/demo_match_integrity/`
  - CLI wrapper: `scripts/demo_match_integrity.py`
- Vertical summary:
  - `docs/GAMING_VERTICAL_SUMMARY.md`

## 3) PQ Demos (this repo)
- PQ narrative:
  - `docs/PQ_DEMO_NARRATIVE.md`
- Hybrid provenance narrative:
  - `docs/HYBRID_PROVENANCE_DEMO.md`
- Historical payload note:
  - `docs/HISTORICAL_VECTOR_RAW.md`
- Fixtures:
  - technical: `fixtures/mldsa/vector_001.json`
  - historical/richer: `fixtures/mldsa/vector_raw.json`

## 4) Hardhat Anchoring Demo
- Minimal on-chain integrity harness:
  - `docs/HARDHAT_TEST_LANE.md`
  - `contracts/ReceiptAnchor.sol`
  - `contracts/GameEventAnchor.sol`
  - `test/ReceiptAnchor.test.js`
  - `test/GameEventAnchor.test.js`

## 5) Outreach Packaging
- Short pitch: `docs/SHORT_PITCH.md`
- Magicians draft: `docs/OUTREACH_POST_MAGICIANS.md`

## 6) Visual Demo Pack
- Threat model: `docs/visuals/THREAT_MODEL.md`
- Audit trail flow: `docs/visuals/AUDIT_TRAIL_FLOW.md`
- Anchoring flow: `docs/visuals/ANCHORING_FLOW.md`
- Screen guide: `docs/visuals/DEMO_SCREEN_GUIDE.md`

## Recommended first outreach flow
1. Match Integrity (3–5 min canonical script)
2. Tamper + continuity fail semantics
3. `vector_raw` provenance bridge over `vector_001`
4. Optional Hardhat anchor + duplicate guard
