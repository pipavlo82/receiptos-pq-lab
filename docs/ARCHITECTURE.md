# Architecture (Phase-1 Draft)

## Objective
Define an optional extension architecture for ReceiptOS that can evolve toward post-quantum trust without breaking the MVP trust layer.

## Layers
1. **Core Receipt Layer (external dependency)**
   - Existing receipt canonicalization/sign/verify from `receiptos-mvp`
2. **Extension Envelope Layer (this repo)**
   - Adds optional extension fields and verification routes
3. **Policy Router Layer**
   - Chooses verification mode: baseline / entropy-augmented / hybrid

## Verification modes
- **baseline**
  - Use core ReceiptOS signature checks only
- **entropy_augmented**
  - Baseline + entropy attest fields + freshness/risk policy checks
- **hybrid**
  - Baseline + entropy fields + optional PQ signature envelope

## Data flow (target)
1. Agent creates decision payload
2. Core receipt is generated (MVP format)
3. Extension envelope attaches:
   - entropy context
   - optional VRF/proof fields
   - optional PQ signer metadata
4. Verifier evaluates according to selected mode
5. Result emits deterministic reason codes + extension reasons

## Integration model with ReceiptOS MVP
- Core receipt schema remains source of truth
- Extension fields are additive and versioned
- Verification can be run in dual mode:
  - `core_verify` result
  - `extension_verify` result

## Proposed extension points
- `receipt_extension.mode`
- `receipt_extension.entropy`
- `receipt_extension.vrf`
- `receipt_extension.pq_signature`
- `receipt_extension.policy_path`

## Safety principles
- Backward-compatible additions only
- No mutation of core MVP semantics
- Explicit downgrade behavior if extension verification unavailable
