# Gaming Demo: Loot Drop Fairness

## Use-case (short)
A player receives a high-value item drop and questions whether the drop was manipulated.

## Problem without ReceiptOS
- Logs can be edited after the fact.
- Randomness claims are hard to verify externally.
- Replay or duplicate award events may slip through in edge failures.

## Flow with ReceiptOS
1. Game service emits `loot_drop` event.
2. Core receipt is created for canonical event payload.
3. Entropy/VRF extension is attached (`mode=entropy_proof`).
4. Optional chain link (`prev_hash`, `seq`) binds to prior event.
5. Verifier returns deterministic reason semantics.

## Where each layer is used
- **Core receipt**: immutable event context (player/session/drop table/item)
- **Entropy proof**: randomness/entropy validity path
- **Hybrid mode**: optional for premium drops (entropy + signature)
- **Chain integrity**: prevents continuity tampering across drop timeline

## Important reason codes / failure cases
- `OK` — baseline successful verification
- `VERIFY_FAILED` — invalid proof / invalid signature semantics
- `MISSING_REQUIRED_FIELD` — missing required payload parts
- `ADAPTER_INVALID_INPUT` — malformed proof/signature shape
- `ADAPTER_INTERNAL_ERROR` — backend unavailable/internal failure

## What to show in a live demo
1. Verify **valid** receipt -> `OK`.
2. Verify **tampered** receipt (item changed post-sign) -> failure (`VERIFY_FAILED` or equivalent).
3. Verify **continuity/replay anomaly** payload -> deterministic fail (continuity mismatch path).
4. Explain that flow is off-chain first and anchoring is optional for periodic checkpoints.
