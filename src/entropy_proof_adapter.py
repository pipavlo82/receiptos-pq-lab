from __future__ import annotations

# Backward-compatibility shim.
# New backend-boundary implementation lives in entropy_adapter.py

from .entropy_adapter import (
    EntropyAdapter as MockEntropyProofAdapter,
    EntropyAdapterContract as EntropyProofAdapter,
    verify_entropy_proof_with_adapter,
)

__all__ = [
    "EntropyProofAdapter",
    "MockEntropyProofAdapter",
    "verify_entropy_proof_with_adapter",
]
