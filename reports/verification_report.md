# Verification Report — Gaming Match Integrity Demo

- with_mirofish_scenarios: **False**
- mirofish_requested: **False**
- mirofish_enabled: **False**
- mirofish_status_reason: `not_requested`
- total_cases: **6**
- passed: **6**
- failed: **0**

## Reason code distribution
- BAD_SIGNATURE: 1
- CHAIN_MISMATCH: 1
- OK: 1
- REPLAY: 1
- TAMPER: 2

## Case-by-case results
| case_id | kind | expected | actual | ok |
|---|---|---|---|---|
| valid_baseline | valid | OK | OK | True |
| tamper_event | tamper | TAMPER | TAMPER | True |
| replay_receipt | replay | REPLAY | REPLAY | True |
| altered_result | tamper | TAMPER | TAMPER | True |
| bad_signature | bad_signature | BAD_SIGNATURE | BAD_SIGNATURE | True |
| chain_mismatch | chain_mismatch | CHAIN_MISMATCH | CHAIN_MISMATCH | True |

## Conclusion
The deterministic verifier correctly distinguishes valid execution history from tamper, replay, bad-signature, and chain-mismatch scenarios using machine-readable reason codes.
This makes the demo externally showable as a proof-of-integrity layer for authoritative match disputes.
