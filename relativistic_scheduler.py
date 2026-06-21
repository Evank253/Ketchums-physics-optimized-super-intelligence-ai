"""
Ketchum's Physics Optimized Super Intelligence
Relativistic Scheduler — v2

PHYSICS:
- Radioactive decay for priority: P(t) = P0 * exp(-lambda*t)
- Lorentz factor for load-based contraction
- Earliest Deadline First scheduling
- Sentence-scoring prompt compression (not truncation)
- Latency percentile tracking
"""

import math
import time
from typing import Optional


class RelativisticScheduler:

    URGENCY = {
        "coding": 1.0, "reasoning": 1.5, "research": 2.0, "creative": 3.0,
        "math": 1.0, "planning": 1.5, "analysis": 1.5, "general": 2.0,
    }
    PRIORITY_HALF_LIFE = 3600.0

    def __init__(self, max_load: float = 1.0):
        self.max_load = max_load
        self.latency_history = []
        self.scheduling_log = []
        self.stats = {
            "schedules": 0, "avg_lorentz_factor": 1.0,
            "avg_contraction": 0.0, "expirations": 0,
            "deadlines_met": 0, "deadlines_missed": 0,
        }

    def calculate_lorentz_factor(self, load: float) -> float:
        v_over_c = min(load * 0.99, 0.999)
        return 1.0 / math.sqrt(1.0 - v_over_c ** 2)

    def priority_decay(self, base_priority: float, age_seconds: float) -> float:
        decay_constant = math.log(2) / self.PRIORITY_HALF_LIFE
        return base_priority * math.exp(-decay_constant * age_seconds)

    def assign_deadline(self, query_type: str, base_deadline_ms: float = 5000.0) -> float:
        return base_deadline_ms * self.URGENCY.get(query_type, 2.0)

    def length_contract_prompt(self, prompt: str, load: float) -> dict:
        gamma = self.calculate_lorentz_factor(load)
        original_length = len(prompt)
        contracted_length = int(original_length / gamma)

        if contracted_length >= original_length:
            return {
                "prompt": prompt, "original_length": original_length,
                "contracted_length": original_length, "contraction_ratio": 0.0,
                "contracted": False, "lorentz_factor": round(gamma, 4), "method": "none",
            }

        sentences = [s.strip() for s in prompt.replace("! ", ". ").replace("? ", ". ").split(". ") if s.strip()]
        if len(sentences) <= 1:
            return {
                "prompt": prompt, "original_length": original_length,
                "contracted_length": original_length, "contraction_ratio": 0.0,
                "contracted": False, "lorentz_factor": round(gamma, 4), "method": "single_sentence",
            }

        scored = []
        for i, sentence in enumerate(sentences):
            score = self._score_sentence(sentence, i, len(sentences))
            scored.append((i, sentence, score))

        scored.sort(key=lambda x: x[2], reverse=True)

        selected = []
        total_len = 0
        for orig_idx, sentence, score in scored:
            if total_len + len(sentence) + 2 <= contracted_length:
                selected.append((orig_idx, sentence))
                total_len += len(sentence) + 2

        selected.sort(key=lambda x: x[0])
        contracted_prompt = ". ".join(s for _, s in selected)
        contraction_ratio = 1.0 - (len(contracted_prompt) / max(original_length, 1))

        self.stats["schedules"] += 1
        self.stats["avg_lorentz_factor"] = round(
            (self.stats["avg_lorentz_factor"] * (self.stats["schedules"] - 1) + gamma) / self.stats["schedules"], 4,
        )
        self.stats["avg_contraction"] = round(
            (self.stats["avg_contraction"] * (self.stats["schedules"] - 1) + contraction_ratio) / self.stats["schedules"], 4,
        )

        return {
            "prompt": contracted_prompt, "original_length": original_length,
            "contracted_length": len(contracted_prompt),
            "contraction_ratio": round(contraction_ratio, 4),
            "contracted": contraction_ratio > 0.05, "lorentz_factor": round(gamma, 4),
            "sentences_kept": len(selected), "sentences_total": len(sentences),
            "method": "sentence_scoring",
        }

    def _score_sentence(self, sentence: str, position: int, total: int) -> float:
        words = sentence.lower().split()
        if not words:
            return 0.0
        position_score = 1.0 if position == 0 else 0.8 if position == total - 1 else 0.5
        unique_ratio = len(set(words)) / max(len(words), 1)
        length_score = 0.2 if len(words) < 3 else 0.6 if len(words) < 10 else 1.0 if len(words) < 20 else 0.8
        return position_score * 0.3 + unique_ratio * 0.4 + length_score * 0.3

    def measure_latency(self, start_time: float, deadline_ms: float = None) -> dict:
        actual_ms = (time.time() - start_time) * 1000
        self.latency_history.append(actual_ms)
        if len(self.latency_history) > 1000:
            self.latency_history = self.latency_history[-1000:]

        sorted_lat = sorted(self.latency_history)
        p50 = sorted_lat[len(sorted_lat) // 2]
        p95 = sorted_lat[int(len(sorted_lat) * 0.95)]
        p99 = sorted_lat[int(len(sorted_lat) * 0.99)]

        met_deadline = True
        if deadline_ms is not None:
            met_deadline = actual_ms <= deadline_ms
            if met_deadline:
                self.stats["deadlines_met"] += 1
            else:
                self.stats["deadlines_missed"] += 1

        return {
            "actual_ms": round(actual_ms, 2), "p50_ms": round(p50, 2),
            "p95_ms": round(p95, 2), "p99_ms": round(p99, 2),
            "met_deadline": met_deadline, "deadline_ms": deadline_ms,
        }

    def get_scheduler_stats(self) -> dict:
        deadline_rate = self.stats["deadlines_met"] / max(
            self.stats["deadlines_met"] + self.stats["deadlines_missed"], 1,
        )
        return {
            **self.stats, "deadline_hit_rate": round(deadline_rate, 4),
            "max_load": self.max_load, "priority_half_life_s": self.PRIORITY_HALF_LIFE,
        }
