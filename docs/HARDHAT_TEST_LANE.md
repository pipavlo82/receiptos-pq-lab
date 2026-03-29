# Hardhat Test Lane (Minimal Anchoring Harness)

## What this lane is
A minimal Ethereum-native test sandbox for anchoring and integrity semantics.

It is **not** a full on-chain verifier and does not implement heavy PQ/VRF cryptography on-chain.

## Why this exists
Current direction is off-chain first. This lane adds just enough on-chain surface to validate:
- anchoring semantics
- duplicate/replay guards
- continuity/ordering checks for game events

## Contracts
- `ReceiptAnchor.sol`
  - `anchorReceipt(bytes32 receiptHash)`
  - `isAnchored(bytes32 receiptHash)`
- `GameEventAnchor.sol`
  - `anchorGameEvent(bytes32 eventHash, uint256 seq, bytes32 prevHash)`
  - `getEventBySeq(uint256 seq)`
  - duplicate hash guard + continuity checks (`seq`, `prevHash`)

## Relation to off-chain first model
- Off-chain stack (ReceiptOS core + extension verification) still does the heavy semantic verification.
- On-chain lane provides anchoring/checkpoint and basic integrity guarantees.
- This is sufficient for demo/value validation before protocol complexity.

## Why this is enough now
- demonstrates Ethereum-native integrity path
- supports gaming demos (loot fairness + match chain integrity)
- avoids premature protocol design and on-chain crypto overhead

## Run (local)
```bash
npm install
npx hardhat test
```
