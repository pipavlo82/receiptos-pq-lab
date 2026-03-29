# Gaming Architecture Lane (Additive)

## Scope
This document defines a gaming vertical architecture within `receiptos-pq-lab`.
It reuses existing core + extension contracts and adds game-event semantics only.

## Layering
1. **Core Receipt Layer (unchanged)**
   - canonical game-event payload
   - signer identity / context
   - baseline verification path
2. **Extension Envelope Layer (unchanged model)**
   - `mode = signature_extension | entropy_proof | hybrid`
   - optional `entropy`, `vrf`, `pq_signature`
3. **Gaming Semantic Layer (new lane)**
   - event classes (loot, match, npc_decision)
   - fairness and integrity tags
   - optional anchoring metadata

## Event Flow
1. Game service emits event payload
2. Core receipt created (game_event type)
3. Optional extension attached:
   - entropy/vrf (fairness path)
   - pq signature (high-assurance path)
   - hybrid (combined)
4. Verifier returns deterministic outputs
5. Optional checkpoint/root anchoring for selected intervals

## How core / entropy / hybrid / chain are used
- **Core receipt**: always required baseline provenance
- **Entropy proof**: fairness-critical randomness validation path
- **Hybrid mode**: high-value or high-risk segments (tournaments, prize drops)
- **Chain integrity**: anti-tamper continuity over event timelines

## Non-goals in this lane
- game engine implementation
- anti-cheat engine replacement
- on-chain contract implementation
- production cryptographic backend in this phase

## Invariants
- Do not break existing extension schema direction
- Keep output contracts stable
- Keep fallback semantics explicit and deterministic
- Keep gaming lane optional and additive
