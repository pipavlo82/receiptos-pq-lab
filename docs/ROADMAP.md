# Roadmap

## Phase 1 — Architecture & Schema Contracts (current)

### Deliverables
- Architecture document with 3 integration models
- Additive extension schema direction (`schemas/receipt_extension.schema.json`)
- Sample payloads for signature-extension / entropy-proof / hybrid
- Interface stubs defining verifier responsibilities

### Exit criteria
- clear core-vs-extension boundary
- deterministic fallback semantics documented
- no compatibility break with baseline ReceiptOS receipt model

---

## Phase 2 — Reference Verification Semantics

### Deliverables
- reference extension verifier stubs in `src/` (still lightweight)
- deterministic extension reason taxonomy
- compatibility fixtures against baseline receipts
- tests for mode routing and degraded/fallback paths

### Exit criteria
- extension paths produce stable outcomes for same inputs
- fallback behavior is explicit (never silent)
- extension checks can be toggled without core breakage

---

## Phase 3 — Experimental Cryptographic Modules

### Deliverables
- optional PQ adapter interface + sample non-production implementation
- optional entropy/VRF adapter interface + sample non-production implementation
- benchmark notes (latency/size/failure behavior)
- decision memo: what is worth upstreaming vs keeping experimental

### Exit criteria
- measurable trust gain vs complexity cost
- documented go/no-go recommendation for production hardening path

---

## Explicit non-goals (for this repo)
- replacing `receiptos-mvp`
- shipping production-grade PQ cryptography in phase-1/2
- enterprise key management platform
- distributed consensus/Byzantine verification systems
- UI/dashboard product layer

This repo is architecture-first R&D for optional trust extensions.
