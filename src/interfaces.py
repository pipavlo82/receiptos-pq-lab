"""Phase-1 interface stubs (no heavy crypto implementation)."""

from __future__ import annotations
from typing import Protocol, Any, Dict


class CoreReceiptVerifier(Protocol):
    def verify_core(self, receipt: Dict[str, Any]) -> Dict[str, Any]: ...


class EntropyVerifier(Protocol):
    def verify_entropy(self, extension: Dict[str, Any]) -> Dict[str, Any]: ...


class VRFVerifier(Protocol):
    def verify_vrf(self, extension: Dict[str, Any]) -> Dict[str, Any]: ...


class PQSignatureVerifier(Protocol):
    def verify_pq_signature(self, extension: Dict[str, Any]) -> Dict[str, Any]: ...


class HybridPolicyRouter(Protocol):
    def select_path(self, extension: Dict[str, Any]) -> str: ...
