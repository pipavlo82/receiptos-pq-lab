# Outreach Monitor v1 (multiplayer segment)

Run:
```bash
python tools/outreach_monitor_v1.py --config docs/market_probe/multiplayer_threads.json
```

Outputs:
- `docs/market_probe/outreach_monitor_report.json`
- `docs/market_probe/outreach_monitor_report.md`

What it does:
- checks configured GitHub threads
- detects non-self replies
- classifies reply (`CONFUSED|INTERESTED|DISMISSIVE|REDIRECT`)
- proposes a concise next-action reply draft

Notes:
- no posting, read-only monitor
- requires authenticated `gh` CLI
