# ReceiptOS PQ Lab

Experimental repository for **post-quantum / entropy / VRF extensions** to ReceiptOS.

## Scope
This repo is **architecture-first** and intentionally separate from the core MVP:
- Base trust layer remains in `receiptos-mvp`
- This repo explores optional extension paths
- No changes are made to core MVP logic from here

## Positioning
- `receiptos-mvp` = baseline verifiable execution layer
- `receiptos-pq-lab` = optional advanced cryptographic extension layer

## Current phase
No heavy cryptographic implementation yet.
Current focus:
1. architecture definition
2. schema extension proposals
3. integration model with ReceiptOS MVP

## Extension tracks
- **Signature path**: alternate signer algorithms and trust policy routing
- **Entropy path**: entropy-backed receipt context for anti-replay/anti-fork hardening
- **Hybrid path**: combine baseline signatures + entropy proofs + optional PQ wrappers

## Repository layout
- `docs/` architecture and roadmap
- `schemas/` extension schema drafts
- `examples/` integration payloads and flow sketches
- `src/` stubs/interfaces only (phase-1)
- `tests/` schema and contract-level tests

## Non-goals (phase-1)
- production deployment
- full PQ stack implementation
- replacing ReceiptOS core MVP

## License
TBD
