"""Conversation state management for guided query flows.

Stores in-memory session state with TTL for multi-turn slot filling.
"""

import threading
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

_STATE_STORE: Dict[str, dict] = {}
_LOCK = threading.Lock()

STATE_TTL_SECONDS = 900  # 15 minutes


def _now() -> datetime:
    return datetime.now()


def _is_expired(state: dict) -> bool:
    expires_at = state.get("expires_at")
    if not expires_at:
        return True
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    return _now() > expires_at


def create_or_update_state(session_id: str, state: dict) -> dict:
    """Create or fully replace session state."""
    now = _now()
    state["session_id"] = session_id
    state["updated_at"] = now.isoformat()
    if "created_at" not in state:
        state["created_at"] = now.isoformat()
    state["expires_at"] = (now + timedelta(seconds=STATE_TTL_SECONDS)).isoformat()
    with _LOCK:
        _STATE_STORE[session_id] = state
    return state


def get_state(session_id: str) -> Optional[dict]:
    """Get session state, returning None if missing or expired."""
    with _LOCK:
        state = _STATE_STORE.get(session_id)
    if state is None:
        return None
    if _is_expired(state):
        clear_state(session_id)
        return None
    return state


def clear_state(session_id: str):
    """Remove session state."""
    with _LOCK:
        _STATE_STORE.pop(session_id, None)


def update_slot(session_id: str, slot_key: str, value: Any, label: str = None):
    """Update a single slot in existing session state."""
    state = get_state(session_id)
    if state is None:
        return None
    collected = state.get("collected_slots", {})
    collected[slot_key] = value
    state["collected_slots"] = collected

    if label:
        labels = state.get("slot_labels", {})
        labels[slot_key] = label
        state["slot_labels"] = labels

    # Remove from missing
    missing = state.get("missing_slots", [])
    if slot_key in missing:
        missing.remove(slot_key)
    state["missing_slots"] = missing

    state["updated_at"] = _now().isoformat()
    state["expires_at"] = (_now() + timedelta(seconds=STATE_TTL_SECONDS)).isoformat()
    with _LOCK:
        _STATE_STORE[session_id] = state
    return state


def cleanup_expired():
    """Remove all expired states. Called periodically if needed."""
    with _LOCK:
        expired_keys = [k for k, v in _STATE_STORE.items() if _is_expired(v)]
        for k in expired_keys:
            del _STATE_STORE[k]
    return len(expired_keys)
