# Gaming Demo: Tournament / Match Integrity

## Use-case (short)
A tournament match result is challenged (winner/score/order integrity dispute).

## Problem without ReceiptOS
- Match events can be claimed but not proven.
- Multi-step lifecycle (start -> updates -> final result) is hard to audit.
- High-stakes disputes need deterministic verification outcomes.

## Flow with ReceiptOS
1. Match lifecycle events generate core receipts.
2. Final result receipt uses `mode=hybrid` for stronger assurance.
3. Entropy/VRF context can cover random map/turn/order selection.
4. PQ signature path covers high-assurance attestation.
5. Chain integrity binds full lifecycle continuity.

## Where each layer is used
- **Core receipt**: canonical match state + result payload
- **Entropy proof**: fairness around randomized competitive parameters
- **Hybrid mode**: strongest demo path (entropy + signature)
- **Chain integrity**: detect missing/reordered/tampered lifecycle entries

## Important reason codes / failure cases
- `OK` — validated event/result chain point
- `HYBRID_PARTIAL_FAILURE` — one sub-path fails in hybrid mode
- `VERIFY_FAILED` — invalid proof/signature semantics
- `MODE_FIELD_MISMATCH` — wrong mode/field contract
- `MISSING_REQUIRED_FIELD` — incomplete receipt payload

## What to show in a live demo
1. Verify **valid hybrid** match receipt -> `OK`.
2. Verify **tampered match result** (winner/score changed) -> fail.
3. Verify **invalid continuity** example (seq/prev_hash mismatch) -> deterministic continuity fail semantics.
4. Highlight deterministic outputs for operator and dispute workflows.
