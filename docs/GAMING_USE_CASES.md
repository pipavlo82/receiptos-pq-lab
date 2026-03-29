# Gaming Use Cases for ReceiptOS PQ Lab

This lane defines a gaming-oriented vertical on top of the existing ReceiptOS extension model.
It does **not** replace core receipt semantics and does **not** modify `receiptos-mvp`.

## 1) Loot / Drop Fairness

### Goal
Prove that loot/drop outcomes were generated under declared randomness and policy constraints.

### Mapping
- **Core receipt:** records event context (player, session, drop table version, seed context hash)
- **Entropy proof path:** validates randomness/entropy proof envelope
- **Hybrid mode:** optional for high-value drops (entropy + signature path)
- **Chain integrity:** ensures event ordering and anti-tamper continuity for drop series

### Why useful
Reduces distrust around manipulated drop rates and supports dispute resolution with verifiable receipts.

---

## 2) Tournament / Match Integrity

### Goal
Create verifiable match lifecycle receipts (start/state transitions/result finalization).

### Mapping
- **Core receipt:** captures authoritative event payloads and result declarations
- **Entropy proof path:** optional randomness attest for map/turn/order selection
- **Hybrid mode:** high-stakes finals / anti-cheat-sensitive events
- **Chain integrity:** binds pre-match, in-match, and post-match events in a deterministic chain

### Why useful
Supports integrity claims for esports ops, audit trails, and anti-dispute replay review.

---

## 3) Off-chain Game Events + Optional On-chain Anchoring

### Goal
Keep operational receipts off-chain for speed/cost, with periodic anchoring for stronger public attestability.

### Mapping
- **Core receipt:** off-chain canonical event receipts
- **Entropy proof path:** optional where event randomness matters
- **Hybrid mode:** optional for prize-impacting event classes
- **Chain integrity:** local chain checkpoints suitable for periodic root anchoring

### Why useful
Practical default: low latency off-chain operations + selective trust amplification via anchoring.

---

## 4) Agent / NPC Decision Receipts

### Goal
Provide provenance for AI-driven NPC/agent decisions (state, input, policy version, output action).

### Mapping
- **Core receipt:** decision payload and action trace
- **Entropy proof path:** optional for stochastic behavior controls
- **Hybrid mode:** optional for competitive or monetized environments
- **Chain integrity:** preserves multi-step behavioral consistency and replay-resistant traces

### Why useful
Turns opaque NPC/agent behavior into verifiable, analyzable execution history.

---

## Integration Notes
- Gaming lane is **additive** and vertical-specific.
- Existing extension modes remain unchanged.
- This lane contributes schemas/examples/docs only (no heavy cryptography introduced).
