"""
Ketchum's Physics Optimized Super Intelligence
Spintronic Memory — v2

PHYSICS:
- MRAM persistence: data survives process restart (SQLite-backed)
- Read/write cost asymmetry: fast read, costly write
- LRU-K access tracking for better eviction
- N-gram vector similarity search
- Priority-based retention like spin alignment strength
"""

import hashlib
import math
import time
import json
import sqlite3
import os
from typing import Optional
from collections import OrderedDict


class SpintronicMemory:

    def __init__(self, max_size: int = 50000, db_path: str = ".spintronic.db"):
        self.max_size = max_size
        self.db_path = db_path
        self.spin_states = OrderedDict()
        self.access_history = {}
        self.lru_k = 3
        self.read_cost_ms = 0.001
        self.write_cost_ms = 1.0

        self._init_db()
        self._load_from_db()

        self.stats = {
            "writes": 0, "reads": 0, "hits": 0, "misses": 0,
            "evictions": 0, "spin_flips": 0, "db_writes": 0,
            "db_reads": 0, "total_write_cost_ms": 0.0, "total_read_cost_ms": 0.0,
        }

    def _init_db(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS spin_states (
                spin_key TEXT PRIMARY KEY,
                value_json TEXT NOT NULL,
                priority REAL DEFAULT 0.5,
                written_at REAL NOT NULL,
                original_key TEXT,
                read_count INTEGER DEFAULT 0
            )
        """)
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_priority ON spin_states(priority)")
        self.conn.commit()

    def _load_from_db(self):
        try:
            cursor = self.conn.execute(
                "SELECT spin_key, value_json, priority, written_at, original_key, read_count "
                "FROM spin_states ORDER BY priority DESC LIMIT ?", (self.max_size,),
            )
            for row in cursor:
                spin_key, value_json, priority, written_at, original_key, read_count = row
                self.spin_states[spin_key] = {
                    "value": json.loads(value_json), "priority": priority,
                    "written_at": written_at, "reads": read_count, "original_key": original_key or "",
                }
        except sqlite3.Error:
            pass

    def _persist_to_db(self, spin_key: str, entry: dict):
        try:
            self.conn.execute("""
                INSERT OR REPLACE INTO spin_states
                (spin_key, value_json, priority, written_at, original_key, read_count)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                spin_key, json.dumps(entry["value"], default=str),
                entry["priority"], entry["written_at"],
                entry.get("original_key", "")[:100], entry.get("reads", 0),
            ))
            self.conn.commit()
            self.stats["db_writes"] += 1
        except sqlite3.Error:
            pass

    def _hash_key(self, key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()[:24]

    def _update_access_history(self, spin_key: str):
        if spin_key not in self.access_history:
            self.access_history[spin_key] = []
        self.access_history[spin_key].append(time.time())
        if len(self.access_history[spin_key]) > self.lru_k:
            self.access_history[spin_key] = self.access_history[spin_key][-self.lru_k:]

    def write(self, key: str, value: any, priority: float = 0.5) -> dict:
        spin_key = self._hash_key(key)
        is_flip = spin_key in self.spin_states
        if is_flip:
            self.stats["spin_flips"] += 1

        entry = {
            "value": value, "priority": priority,
            "written_at": time.time(), "reads": 0, "original_key": key[:100],
        }
        self.spin_states[spin_key] = entry
        self._update_access_history(spin_key)
        self._persist_to_db(spin_key, entry)

        self.stats["writes"] += 1
        self.stats["total_write_cost_ms"] += self.write_cost_ms

        while len(self.spin_states) > self.max_size:
            self._evict_lowest_priority()

        return {"written": True, "is_flip": is_flip, "spin_key": spin_key}

    def read(self, key: str) -> Optional[any]:
        spin_key = self._hash_key(key)
        self.stats["reads"] += 1
        self.stats["total_read_cost_ms"] += self.read_cost_ms

        if spin_key in self.spin_states:
            self.stats["hits"] += 1
            entry = self.spin_states[spin_key]
            entry["reads"] += 1
            self._update_access_history(spin_key)
            entry["priority"] = min(1.0, entry["priority"] + 0.01)
            self.spin_states.move_to_end(spin_key)
            return entry["value"]

        try:
            cursor = self.conn.execute("SELECT value_json FROM spin_states WHERE spin_key = ?", (spin_key,))
            row = cursor.fetchone()
            if row:
                self.stats["db_reads"] += 1
                value = json.loads(row[0])
                self.spin_states[spin_key] = {
                    "value": value, "priority": 0.5,
                    "written_at": time.time(), "reads": 1, "original_key": key[:100],
                }
                return value
        except sqlite3.Error:
            pass

        self.stats["misses"] += 1
        return None

    def bulk_search(self, query: str, max_results: int = 5) -> list:
        query_vector = self._text_to_vector(query)
        query_lower = query.lower()
        results = []

        for spin_key, entry in self.spin_states.items():
            original = entry.get("original_key", "")
            entry_vector = self._text_to_vector(original)
            similarity = self._cosine_similarity(query_vector, entry_vector)
            words_match = sum(1 for w in query_lower.split() if w in original.lower())
            combined_score = similarity * 0.7 + min(words_match / max(len(query_lower.split()), 1), 1.0) * 0.3

            if combined_score > 0.1:
                results.append({
                    "key": original, "value": entry["value"],
                    "similarity": round(similarity, 4), "keyword_match": words_match,
                    "combined_score": round(combined_score, 4), "priority": entry["priority"],
                })

        results.sort(key=lambda x: (x["combined_score"], x["priority"]), reverse=True)
        return results[:max_results]

    def _text_to_vector(self, text: str) -> dict:
        if not text:
            return {}
        text_lower = text.lower()
        vector = {}
        for i in range(len(text_lower) - 1):
            bigram = text_lower[i:i + 2]
            vector[bigram] = vector.get(bigram, 0) + 1
        for i in range(len(text_lower) - 2):
            trigram = text_lower[i:i + 3]
            vector[trigram] = vector.get(trigram, 0) + 1
        for word in text_lower.split():
            vector[f"w:{word}"] = vector.get(f"w:{word}", 0) + 2
        return vector

    def _cosine_similarity(self, vec_a: dict, vec_b: dict) -> float:
        if not vec_a or not vec_b:
            return 0.0
        common_keys = set(vec_a.keys()) & set(vec_b.keys())
        dot = sum(vec_a[k] * vec_b[k] for k in common_keys)
        mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
        mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))
        if mag_a == 0 or mag_b == 0:
            return 0.0
        return dot / (mag_a * mag_b)

    def _evict_lowest_priority(self):
        if not self.spin_states:
            return
        now = time.time()
        scores = {}
        for spin_key, entry in self.spin_states.items():
            base = entry["priority"]
            if spin_key in self.access_history and self.access_history[spin_key]:
                kth_access = self.access_history[spin_key][0]
                recency = 1.0 / (1.0 + (now - kth_access) / 3600.0)
            else:
                recency = 0.1
            scores[spin_key] = base * 0.6 + recency * 0.4

        lowest_key = min(scores, key=scores.get)
        del self.spin_states[lowest_key]
        self.access_history.pop(lowest_key, None)
        try:
            self.conn.execute("DELETE FROM spin_states WHERE spin_key = ?", (lowest_key,))
            self.conn.commit()
        except sqlite3.Error:
            pass
        self.stats["evictions"] += 1

    def verify_nonvolatility(self) -> dict:
        try:
            cursor = self.conn.execute("SELECT COUNT(*) FROM spin_states")
            db_count = cursor.fetchone()[0]
        except sqlite3.Error:
            db_count = 0
        return {"memory_entries": len(self.spin_states), "db_entries": db_count, "is_nonvolatile": db_count > 0}

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass

    def get_stats(self) -> dict:
        hit_rate = self.stats["hits"] / max(self.stats["reads"], 1)
        return {
            **self.stats, "hit_rate": round(hit_rate, 4),
            "stored": len(self.spin_states), "capacity": self.max_size,
            "utilization": round(len(self.spin_states) / self.max_size, 4),
            "avg_write_cost_ms": round(self.stats["total_write_cost_ms"] / max(self.stats["writes"], 1), 4),
            "avg_read_cost_ms": round(self.stats["total_read_cost_ms"] / max(self.stats["reads"], 1), 4),
            "write_read_cost_ratio": round(self.write_cost_ms / self.read_cost_ms, 1),
        }
