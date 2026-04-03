# receiptos_gaming_integrity_mvp

Message:
"We resolve match disputes with verifiable execution receipts."

Case:
Player claims match was manipulated.

Run:
python demo/match_simulator.py
python demo/generate_receipts.py
python demo/verify.py all

Single-command demo:
python demo/match_simulator.py && python demo/generate_receipts.py && python demo/verify.py all

Example (tamper case):
python demo/verify.py data/tampered_event_chain.json

Output:
FAIL — tamper detected at event #4

Conclusion:
match execution was altered

What files are produced:
- data/valid_receipt_chain.json
- data/tampered_event_chain.json
- data/replay_injected_chain.json
- output/verification_report.md
