# ReceiptOS PQ Lab

[![Status](https://img.shields.io/badge/status-experimental-blue)](#)
[![Mode](https://img.shields.io/badge/off--chain-first-6f42c1)](#)
[![Focus](https://img.shields.io/badge/focus-adapter%20boundaries-0a7ea4)](#)

`receiptos-pq-lab` is an **optional extension lab** for post-quantum and entropy/VRF trust paths on top of ReceiptOS.

## Start here (most important)

### 3–5 min canonical demo
- Script command: `python3 scripts/demo_match_integrity.py`
- Walkthrough: [DEMO_MATCH_INTEGRITY_SCRIPT.md](docs/DEMO_MATCH_INTEGRITY_SCRIPT.md)
- Core scenario: valid -> tamper fail -> continuity fail

### Key fixtures
- Technical fixture: [vector_001.json](fixtures/mldsa/vector_001.json)
- Historical/provenance fixture: [vector_raw.json](fixtures/mldsa/vector_raw.json)

### Key narratives
- PQ narrative: [PQ_DEMO_NARRATIVE.md](docs/PQ_DEMO_NARRATIVE.md)
- Hybrid provenance narrative: [HYBRID_PROVENANCE_DEMO.md](docs/HYBRID_PROVENANCE_DEMO.md)
- Short pitch: [SHORT_PITCH.md](docs/SHORT_PITCH.md)
- Magicians outreach draft: [OUTREACH_POST_MAGICIANS.md](docs/OUTREACH_POST_MAGICIANS.md)

### Visual demo pack
- [THREAT_MODEL.md](docs/visuals/THREAT_MODEL.md)
- [AUDIT_TRAIL_FLOW.md](docs/visuals/AUDIT_TRAIL_FLOW.md)
- [ANCHORING_FLOW.md](docs/visuals/ANCHORING_FLOW.md)
- [DEMO_SCREEN_GUIDE.md](docs/visuals/DEMO_SCREEN_GUIDE.md)

---

## Why this repo exists
`receiptos-mvp` is the baseline trust layer (sign/verify/replay/chain).

This repo answers a separate question:
> How do we evolve toward stronger cryptographic trust **without breaking** the baseline MVP contract?

---

## What this is (and is not)

### ✅ This repo is
- an additive extension architecture and integration lab
- a place for stable adapter/backend contracts
- a demo/outreach-ready PQ + provenance + gaming vertical sandbox

### ❌ This repo is not
- a replacement for `receiptos-mvp`
- a production-complete PQ verifier package
- a heavy on-chain cryptography repo

---

## Current implementation status

### Implemented now
- Additive extension schema direction (`signature_extension`, `entropy_proof`, `hybrid`)
- Reference verifier layer (deterministic mode routing + failure semantics)
- Adapter contract layer + reason normalization taxonomy
- ML-DSA backend boundary (transitional real path wiring)
- Fixture loaders:
  - technical: `fixtures/mldsa/vector_001.json`
  - historical/provenance-rich: `fixtures/mldsa/vector_raw.json`
- Gaming vertical lane (loot fairness, match integrity, NPC provenance)
- Minimal Hardhat anchoring lane (receipt/event anchoring + continuity guards)
- Demo packaging docs + scripts for outreach

### Still transitional
- Full production-grade ML-DSA runtime verification in this repo
- Full cryptographic backend hardening and ops policies

---

## Core boundary model
- **Core receipt (source of truth):** remains in `receiptos-mvp`
- **Extension envelope (optional/additive):** lives here
- **Output invariants:** stable normalized verification shapes + deterministic reason codes

---

## Quick navigation
- Architecture: [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Roadmap: [ROADMAP.md](docs/ROADMAP.md)
- Adapter contracts: [ADAPTER_INTERFACES.md](docs/ADAPTER_INTERFACES.md)
- ML-DSA real path notes: [MLDSA_REAL_BACKEND_PATH.md](docs/MLDSA_REAL_BACKEND_PATH.md)
- Demo index: [DEMO_INDEX.md](docs/DEMO_INDEX.md)
- Hardhat lane: [HARDHAT_TEST_LANE.md](docs/HARDHAT_TEST_LANE.md)

---

## Positioning sentence
- `receiptos-mvp` = baseline verifiable execution layer
- `receiptos-pq-lab` = optional advanced trust extension R&D (PQ/entropy/VRF)
