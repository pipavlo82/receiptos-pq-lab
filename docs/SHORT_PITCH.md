# Short Pitch

## One-liner
ReceiptOS turns off-chain events into verifiable execution receipts with deterministic integrity outcomes.

## Problem
Game events and other off-chain execution flows are usually logged, not provable.
That makes tamper/replay/continuity disputes hard to resolve.

## Solution
ReceiptOS adds:
- canonical receipts,
- optional entropy/PQ extension paths,
- chain continuity semantics,
- deterministic reason-coded verification outcomes.

## What is new
- Hybrid model: off-chain verification first, optional on-chain anchoring
- PQ-ready verification layer via stable adapter/backend boundaries

## Demo
- Match Integrity scenario
- tamper detection
- replay/continuity failure signaling
