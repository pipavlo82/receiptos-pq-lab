# Architecture (Phase-1)

## Objective
Define a safe, additive extension architecture for ReceiptOS that can evolve toward post-quantum and entropy-backed verification while preserving baseline compatibility.

---

## Layered model
1. **Core Receipt Layer (external, stable)**
   - canonical receipt payload
   - baseline sign/verify semantics
2. **Extension Envelope Layer (this repo)**
   - optional extension fields and mode metadata
3. **Verification Policy Layer**
   - chooses path: signature-extension / entropy-proof / hybrid

Design rule: extension outcomes must be explainable without mutating core receipt semantics.

---

## Integration Model A: Signature Extension Path

### What is added to receipt
Optional envelope fields:
- `receipt_extension.mode = "signature_extension"`
- `receipt_extension.pq_signature.*`
- `receipt_extension.policy_path.*`

### What is verified locally
- core receipt verify remains mandatory
- extension verifies signature metadata presence/format
- policy router decides whether extension signature is required or advisory

### Out of MVP scope
- full ML-DSA/Falcon/SPHINCS+ production verification
- key custody lifecycle / HSM routing
- hardware-backed trust roots

### Risks / failure modes
- key format mismatch between environments
- false sense of security if extension signature is marked optional but interpreted as mandatory by downstream users
- trust-policy drift (`required` vs `advisory`) across services

---

## Integration Model B: Entropy Proof Path

### What is added to receipt
Optional envelope fields:
- `receipt_extension.mode = "entropy_proof"`
- `receipt_extension.entropy.*`
- `receipt_extension.vrf.*` (optional in this mode)
- `receipt_extension.policy_path.*`

### What is verified locally
- core receipt verify remains mandatory
- entropy payload structure and freshness window checks
- policy checks over entropy score bounds and recency
- optional VRF proof-format gate (not full cryptographic proof verification in phase-1)

### Out of MVP scope
- cryptographic entropy attestation guarantees
- distributed randomness beacon trust assumptions
- formal anti-bias guarantees for entropy sources

### Risks / failure modes
- stale entropy accepted due to weak freshness policy
- entropy source spoofing if provenance not pinned
- over-reliance on entropy score without calibration

---

## Integration Model C: Hybrid Path

### What is added to receipt
Optional envelope fields:
- `receipt_extension.mode = "hybrid"`
- `pq_signature + entropy + optional vrf`
- explicit `policy_path` with fallback semantics

### What is verified locally
- baseline core verification
- extension field coherence checks
- path selection determinism (`selected_path`, `fallback_path`, `reason`)
- deterministic extension reason codes for partial/fallback outcomes

### Out of MVP scope
- formally secure composition proof of entropy + PQ
- distributed verifier consensus
- production-grade failover orchestration

### Risks / failure modes
- ambiguous downgrade behavior (silent fallback)
- inconsistent verifier implementations between services
- operational complexity increases faster than trust gain

---

## Additive compatibility contract
- Core receipt remains valid with no extension.
- Extension fields are optional and versioned.
- Missing extension must not break baseline verification.
- Any extension failure must produce deterministic extension-level reason semantics.

---

## Failure semantics (target)
Core outcome and extension outcome should be separable:
- `core_verify`: pass/fail
- `extension_verify`: pass/fail/degraded/not_applicable

This enables safe rollout without forcing all consumers into extension mode.
