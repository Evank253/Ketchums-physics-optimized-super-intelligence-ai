"""
Ketchum's Physics Optimized Super Intelligence
Key-Value Memory Store — v2
"""

from typing import Optional
from collections import OrderedDict


_memory = OrderedDict()
_max_size = 10000


def add(key: str, value: Optional[str] = None) -> dict:
    if value is not None:
        _memory[key] = value
    else:
        _memory[key] = True
    while len(_memory) > _max_size:
        _memory.popitem(last=False)
    return {"stored": True, "key": key[:100]}


def retrieve(key: str) -> Optional[str]:
    if key in _memory:
        value = _memory[key]
        _memory.move_to_end(key)
        return value if isinstance(value, str) else str(value)
    key_lower = key.lower()
    for stored_key, value in reversed(_memory.items()):
        if key_lower in stored_key.lower() or stored_key.lower() in key_lower:
            return value if isinstance(value, str) else str(value)
    return None


def search(query: str, max_results: int = 5) -> list:
    query_lower = query.lower()
    results = []
    for key, value in _memory.items():
        if query_lower in key.lower() or key.lower() in query_lower:
            results.append({"key": key[:100], "value": value})
    return results[:max_results]


def clear():
    _memory.clear()


def get_stats() -> dict:
    return {"entries": len(_memory), "max_size": _max_size,
            "utilization": round(len(_memory) / _max_size, 4)}
