from pathlib import Path


def test_layout_exists():
    root = Path(__file__).resolve().parents[1]
    for p in [
        root / 'README.md',
        root / 'docs' / 'ARCHITECTURE.md',
        root / 'docs' / 'ROADMAP.md',
        root / 'schemas' / 'receipt_extension.schema.json',
        root / 'examples' / 'extension_payload.sample.json',
        root / 'src' / 'interfaces.py',
    ]:
        assert p.exists(), f"missing: {p}"
