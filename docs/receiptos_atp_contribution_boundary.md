# ReceiptOS / ATP Contribution Boundary Note

_Date: 2026-05-28 (snapshot audit)_

## Purpose
This note documents prior independent ReceiptOS work and defines a clean collaboration boundary before any ATP/CYPHES integration discussion.

## Public repo snapshot (read-only evidence)

### 1) ReceiptOS MVP
- Repo: https://github.com/pipavlo82/receiptos-mvp
- API repo metadata URL: https://api.github.com/repos/pipavlo82/receiptos-mvp
- Default branch: `main`
- HEAD commit (main): `0e70ebe85f4dd1b8b2a24be9c29f1b9757e25a71`
- Created: 2026-03-29T16:41:20Z
- Last pushed: 2026-03-29T20:10:04Z

README (summary):
- Positions ReceiptOS as a trust/verifiable execution layer for agent tool calls.
- Claims signed receipts, replay/tamper detection, hash-chain verification, deterministic reason codes.
- Includes CLI/API flows (`sign`, `verify`, `verify-chain`) and demo scripts (codex/tamper/replay).

Observed schema/tests/feature artifacts from public tree:
- `schemas/decision_receipt.schema.json`
- `tests/test_smoke.py`
- `tests/test_reason_codes.py`
- `src/api.py`, `src/cli.py`, `src/receiptos.py`
- `examples/replay_demo.py`, `examples/tamper_demo.py`, `examples/codex_agent_demo.py`

LICENSE:
- No root `LICENSE` file found at `main/LICENSE` in this snapshot (404 on direct raw lookup).

---

### 2) ReceiptOS-PQ Lab
- Repo: https://github.com/pipavlo82/receiptos-pq-lab
- API repo metadata URL: https://api.github.com/repos/pipavlo82/receiptos-pq-lab
- Default branch: `main`
- HEAD commit (main): `c50db1169a9218bc91fdc54459eb47e45d3c5894`
- Created: 2026-03-29T17:23:32Z
- Last pushed: 2026-05-03T20:28:38Z

README (summary):
- Presents ReceiptOS-PQ as verifiable match/execution integrity with deterministic reason-coded verdicts.
- Emphasizes crypto-agility thesis: versioned verification lanes, hybrid migration paths, policy-driven verifier upgrades.
- Explicitly demonstrates tamper/replay/bad-signature/chain mismatch detection.

Observed schema/tests/feature-adjacent artifacts from public tree:
- Demo and verification pipeline files under `demo/` (`run_demo.py`, `verify.py`, `verify_demo.py`, etc.)
- Dispute and chain artifacts under `artifacts/demo_run/`
- Architecture/integration docs under `docs/`
- Solidity anchor contracts under `contracts/`

LICENSE:
- No root `LICENSE` file found at `main/LICENSE` in this snapshot (404 on direct raw lookup).

---

## Positioning boundary (collaboration-safe)

1. **Independent prior work**
   - ReceiptOS and ReceiptOS-PQ existed publicly and independently prior to ATP collaboration discussion.

2. **ReceiptOS-PQ focus area**
   - External receipt verification
   - Deterministic reason codes
   - Tamper/replay detection
   - Signer trust checks
   - Chain continuity
   - Schema validation
   - Crypto-agile / PQ-ready verification lanes

3. **ATP / CYPHES apparent focus area (high-level)**
   - Agent transaction lifecycle
   - Context leases / lease boundaries
   - Settlement orchestration
   - Proof-of-Cognition receipt structure

4. **Natural collaboration surface**
   - ATP/CYPHES receipt output can be treated as input to a ReceiptOS-PQ-style independent verifier.

5. **Ownership clarity**
   - Discussion/exploration does **not** imply ownership transfer.
   - Any shared implementation should be explicitly tracked via written agreement and/or auditable PR/commit history.
   - If scope widens, use a dedicated integration repository to preserve clear authorship boundaries.

## Suggested collaboration protocol
- Keep core repos separate.
- Define a narrow interface spec (receipt schema + verifier contract + reason code mapping).
- Implement adapter/integration layer in a separate repo or clearly scoped PR track.
- Require explicit authorship and license terms before merging cross-project core logic.

