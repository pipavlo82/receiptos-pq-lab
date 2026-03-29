# Roadmap

## Phase 1 — Architecture & Contracts (now)
- Define extension architecture
- Draft schema extensions
- Define integration contract with `receiptos-mvp`
- Add contract tests for additive compatibility

Deliverables:
- `docs/ARCHITECTURE.md`
- schema drafts in `schemas/`
- interface stubs in `src/`

## Phase 2 — Reference Verification Paths
- Implement extension verifier stubs:
  - entropy checks
  - policy path selection
  - hybrid verify orchestration
- Add deterministic extension reason codes
- Add compatibility fixtures against core ReceiptOS receipts

Deliverables:
- `src/` reference verifier modules
- `tests/` path and compatibility tests
- example end-to-end extension payloads

## Phase 3 — PQ/VRF Experimental Modules
- Add optional PQ signature adapter interface
- Add optional VRF proof adapter interface
- Benchmark extension overhead and failure modes
- Document production-readiness criteria

Deliverables:
- adapter interfaces + sample plugin implementations
- benchmark notes
- go/no-go checklist for upstreaming optional features
