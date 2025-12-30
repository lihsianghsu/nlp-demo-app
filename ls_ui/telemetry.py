import streamlit as st
import time
from collections import defaultdict

# In-memory counters (process-local)
_EVENTS = defaultdict(int)
_ERRORS = defaultdict(int)
_LATENCIES = defaultdict(list)

def _enabled():
    return st.session_state.get("ls_telemetry_enabled", True)

def record_event(name: str):
    if not _enabled():
        return
    _EVENTS[name] += 1

def record_error(name: str):
    if not _enabled():
        return
    _ERRORS[name] += 1

def record_latency(name: str, seconds: float):
    if not _enabled():
        return
    _LATENCIES[name].append(round(seconds, 3))

def snapshot():
    """Safe aggregated view"""
    return {
        "events": dict(_EVENTS),
        "errors": dict(_ERRORS),
        "latency_avg": {
            k: round(sum(v) / len(v), 3)
            for k, v in _LATENCIES.items()
            if v
        }
    }
