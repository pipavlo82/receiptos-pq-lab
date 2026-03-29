# ReceiptOS PQ Lab

`receiptos-pq-lab` is an **experimental architecture repository** for optional post-quantum and entropy-proof extensions to ReceiptOS.

## Why this repo exists
ReceiptOS MVP (`receiptos-mvp`) is the baseline trust layer: sign, verify, replay detection, chain checks.

This repo exists to answer a separate question:
> How do we extend ReceiptOS toward stronger cryptographic trust (PQ/entropy/VRF) **without breaking** the core MVP contract?

## How this differs from `receiptos-mvp`
- **receiptos-mvp**
  - product shell + demo-ready trust layer
  - pragmatic baseline verification
  - stable interface for outreach
- **receiptos-pq-lab**
  - architecture + schema + interface lab
  - optional extension envelope design
  - failure semantics and integration strategy first

No core MVP mutation is required for work in this repo.

## What “PQ / entropy / VRF extension layer” means
An **additive envelope** attached to (or referenced by) a core receipt, with optional fields for:
- alternate signature tracks (PQ-ready path)
- entropy/freshness attestations
- VRF-style proof context
- policy routing metadata for verifier behavior

## Core vs optional boundary
- **Core receipt (source of truth):** stays in ReceiptOS MVP contract
- **Extension envelope (optional):** can be absent, partial, or mode-specific
- **Verification model:**
  - baseline-only is always valid
  - extension checks can be enabled by policy
  - downgrade behavior must be explicit and auditable

## Current status (architecture-first)
This repo intentionally avoids heavy crypto implementation right now.

Current focus:
1. architecture and integration contracts
2. additive schema direction
3. failure semantics and mode routing

## Repository layout
- `docs/ARCHITECTURE.md` — integration models and failure semantics
- `docs/ROADMAP.md` — phased plan + explicit non-goals
- `schemas/` — additive extension schema drafts
- `examples/` — sample extension payloads (pq / entropy / hybrid)
- `src/` — interface stubs only
- `tests/` — structure/contract-level checks

## Non-goals (current phase)
- production cryptography implementation
- replacing core ReceiptOS MVP
- enterprise deployment hardening

## Positioning
Use this repo as a **serious optional extension lab**, not as a replacement product.

Core statement:
- `receiptos-mvp` = baseline verifiable execution layer
- `receiptos-pq-lab` = optional advanced trust extension R&D
