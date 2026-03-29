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
  - `examples/gaming/demo_match_integrity/`
- Vertical summary:
  - `docs/GAMING_VERTICAL_SUMMARY.md`

## 3) PQ Demos (this repo)
- PQ narrative:
  - `docs/PQ_DEMO_NARRATIVE.md`
- Hybrid provenance narrative:
  - `docs/HYBRID_PROVENANCE_DEMO.md`
- Fixtures:
  - technical: `fixtures/mldsa/vector_001.json`
  - historical: `fixtures/mldsa/vector_raw.json`

## 4) Hardhat Anchoring Demo
- Minimal on-chain integrity harness:
  - `docs/HARDHAT_TEST_LANE.md`
  - `contracts/ReceiptAnchor.sol`
  - `contracts/GameEventAnchor.sol`
  - `test/ReceiptAnchor.test.js`
  - `test/GameEventAnchor.test.js`

## Recommended first outreach flow
1. MVP baseline trust primitive
2. Gaming vertical (match integrity first)
3. PQ fixture + historical provenance pairing
4. Hardhat anchoring as Ethereum-native extension
