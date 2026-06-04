from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_hex_obj(obj: Any) -> str:
    return sha256_hex_text(canonical(obj))


REQUIRED_TOP_LEVEL = [
    "schema",
    "session_id",
    "directory",
    "task",
    "agent",
    "scope",
    "commands",
    "changes",
    "metadata",
]


def _fail(reason_code: str, fail_path: str | None, details: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "valid": False,
        "reason_code": reason_code,
        "checks": {
            "schema": False,
            "receipt_hash": False,
            "event_root": False,
            "scope": False,
            "commands": False,
            "diff_commitment": False,
        },
        "fail_path": fail_path,
        "details": details,
        "receipt": None,
        "receiptHash": None,
        "eventRoot": None,
    }


def _validate_required(evidence: Dict[str, Any]) -> tuple[bool, str | None, str | None]:
    for field in REQUIRED_TOP_LEVEL:
        if field not in evidence:
            return False, field, f"missing top-level field: {field}"
    if evidence.get("schema") != "stealth.session.evidence.v0":
        return False, "schema", "unexpected schema"
    if not isinstance(evidence.get("commands"), list):
        return False, "commands", "commands must be a list"
    if not isinstance(evidence.get("changes"), dict):
        return False, "changes", "changes must be an object"
    if not isinstance(evidence.get("metadata"), dict):
        return False, "metadata", "metadata must be an object"
    if not isinstance(evidence.get("agent"), dict):
        return False, "agent", "agent must be an object"
    if not isinstance(evidence.get("task"), dict):
        return False, "task", "task must be an object"
    return True, None, None


def _build_transcript(commands: List[Dict[str, Any]], changes: Dict[str, Any], metadata: Dict[str, Any]) -> tuple[List[Dict[str, Any]], str]:
    transcript: List[Dict[str, Any]] = []
    prev_hash = "GENESIS"
    for idx, command in enumerate(commands, start=1):
        if "seq" in command and command["seq"] != idx:
            raise ValueError(f"command seq mismatch at index {idx}")
        cmd = command.get("command")
        if not isinstance(cmd, str) or not cmd.strip():
            raise KeyError(f"commands[{idx-1}].command")
        payload = {
            "command": cmd,
            "exit_code": command.get("exit_code"),
            "stdout_summary": command.get("stdout_summary"),
        }
        event = {
            "seq": idx,
            "type": "command",
            "command": payload,
            "prev_hash": prev_hash,
        }
        event_hash = sha256_hex_obj(event)
        transcript.append({**event, "event_hash": event_hash})
        prev_hash = event_hash

    change_payload = {
        "files_changed": changes.get("files_changed", []),
        "diff_sha256": changes.get("diff_sha256"),
        "diff_count": metadata.get("diff_count"),
    }
    change_event = {
        "seq": len(commands) + 1,
        "type": "change",
        "change": change_payload,
        "prev_hash": prev_hash,
    }
    event_hash = sha256_hex_obj(change_event)
    transcript.append({**change_event, "event_hash": event_hash})
    return transcript, event_hash


def adapt_stealth_handoff_evidence(evidence: Dict[str, Any]) -> Dict[str, Any]:
    try:
        ok, field, message = _validate_required(evidence)
        if not ok:
            return _fail("TAMPER", field, {"error": message})

        transcript, event_root = _build_transcript(
            evidence["commands"],
            evidence["changes"],
            evidence["metadata"],
        )

        receipt = {
            "source": "STEALTH_HANDOFF",
            "transactionId": evidence["session_id"],
            "directory": evidence["directory"],
            "task": evidence["task"],
            "agent": evidence["agent"],
            "scope": evidence["scope"],
            "changed": evidence["changes"],
            "metadata": evidence["metadata"],
            "eventRoot": event_root,
        }
        receipt_hash = sha256_hex_obj(receipt)

        checks = {
            "schema": True,
            "receipt_hash": True,
            "event_root": True,
            "scope": True,
            "commands": True,
            "diff_commitment": "diff_sha256" in evidence.get("changes", {}),
        }

        full_receipt = {
            **receipt,
            "receiptHash": receipt_hash,
        }

        return {
            "valid": True,
            "reason_code": "OK",
            "checks": checks,
            "fail_path": None,
            "details": {
                "source": "STEALTH_HANDOFF",
                "transcript": transcript,
            },
            "receipt": full_receipt,
            "receiptHash": receipt_hash,
            "eventRoot": event_root,
        }
    except KeyError as exc:
        return _fail("TAMPER", str(exc).strip("'"), {"error": "missing required command field"})
    except ValueError as exc:
        return _fail("CHAIN_MISMATCH", "commands", {"error": str(exc)})
    except Exception as exc:
        return _fail(
            "ADAPTER_INTERNAL_ERROR",
            None,
            {"error": "adapter_internal_error", "error_type": type(exc).__name__},
        )
