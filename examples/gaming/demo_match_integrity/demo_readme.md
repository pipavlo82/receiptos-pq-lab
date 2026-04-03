# Gaming Match Integrity Demo

Message:
"We resolve match disputes with verifiable execution receipts."

Case:
Player claims match was manipulated.

Run:
python match_simulator.py
python generate_receipts.py
python verify.py all

Single-command demo:
python match_simulator.py && python generate_receipts.py && python verify.py all

Example:
python verify.py tampered_event_chain.json

Output:
FAIL — tamper detected at event #4

Conclusion:
match execution was altered
