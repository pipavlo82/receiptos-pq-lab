# Verification Report

Case: Player claims match was manipulated.

- `valid_receipt_chain.json`: PASS — PASS — receipt chain valid (no tamper/replay/continuity breaks)
- `tampered_event_chain.json`: FAIL — tamper detected at event #4: hash mismatch
- `replay_injected_chain.json`: FAIL — replay detected at event #5: duplicate event_id=4

Conclusion:
- Invalid chains are clearly rejected with human-readable reason.
- This demo proves altered/replayed execution can be detected.
