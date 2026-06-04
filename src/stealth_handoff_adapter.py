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


def _validate_required(evidence: Dict[str, Any]) -> tuple[bool, str | None, str | None, str | None]:
    if not isinstance(evidence, dict):
        return False, "BAD_SCHEMA", None, "evidence must be an object"
    for field in REQUIRED_TOP_LEVEL:
        if field not in evidence:
            return False, "MISSING_REQUIRED_FIELD", field, f"missing top-level field: {field}"
    if evidence.get("schema") != "stealth.session.evidence.v0":
        return False, "BAD_SCHEMA", "schema", "unexpected schema"
    if not isinstance(evidence.get("commands"), list):
        return False, "BAD_SCHEMA", "commands", "commands must be a list"
    if not isinstance(evidence.get("changes"), dict):
        return False, "BAD_SCHEMA", "changes", "changes must be an object"
    if not isinstance(evidence.get("metadata"), dict):
        return False, "BAD_SCHEMA", "metadata", "metadata must be an object"
    if not isinstance(evidence.get("agent"), dict):
        return False, "BAD_SCHEMA", "agent", "agent must be an object"
    if not isinstance(evidence.get("task"), dict):
        return False, "BAD_SCHEMA", "task", "task must be an object"
    if not isinstance(evidence.get("scope"), dict):
        return False, "BAD_SCHEMA", "scope", "scope must be an object"
    changes = evidence.get("changes", {})
    files_changed = changes.get("files_changed", [])
    if not isinstance(files_changed, list):
        return False, "BAD_SCHEMA", "changes.files_changed", "files_changed must be a list"
    diff_sha256 = changes.get("diff_sha256")
    if diff_sha256 is not None and not isinstance(diff_sha256, str):
        return False, "DIFF_MISMATCH", "changes.diff_sha256", "diff_sha256 must be null or string"
    if isinstance(diff_sha256, str) and not diff_sha256.strip():
        return False, "DIFF_MISMATCH", "changes.diff_sha256", "diff_sha256 cannot be empty"
    if files_changed and diff_sha256 is None:
        return False, "DIFF_MISMATCH", "changes.diff_sha256", "diff_sha256 required when files_changed is non-empty"
    if len(evidence.get("commands", [])) == 0 and not files_changed and diff_sha256 is None:
        return False, "EMPTY_TRANSCRIPT", "commands", "no command events and no change event"
    return True, None, None, None


def _build_transcript(commands: List[Dict[str, Any]], changes: Dict[str, Any], metadata: Dict[str, Any]) -> tuple[List[Dict[str, Any]], str]:
    transcript: List[Dict[str, Any]] = []
    prev_hash = "GENESIS"
    for idx, command in enumerate(commands, start=1):
        if not isinstance(command, dict):
            raise TypeError(f"commands[{idx-1}] must be an object")
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
        ok, reason_code, field, message = _validate_required(evidence)
        if not ok:
            return _fail(reason_code or "ADAPTER_INTERNAL_ERROR", field, {"error": message})

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
    except TypeError as exc:
        return _fail("BAD_SCHEMA", "commands", {"error": str(exc)})
    except Exception as exc:
        return _fail(
            "ADAPTER_INTERNAL_ERROR",
            None,
            {"error": "adapter_internal_error", "error_type": type(exc).__name__},
        )
