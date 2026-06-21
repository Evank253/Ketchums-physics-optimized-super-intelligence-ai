"""
Ketchum's Physics Optimized Super Intelligence
Analog Differential Scorer — v2

Continuous quality scoring with damped feedback.
"""

import math
import numpy as np
from typing import Optional


class AnalogDifferentialScorer:

    def __init__(self):
        self.score_history = []
        self.stats = {"scores_computed": 0, "avg_score": 0.0}

    def continuous_score(self, response: str, query_type: str,
                         prev_score: float = 0.0, damping: float = 0.3) -> dict:
        self.stats["scores_computed"] += 1
        if not response:
            return {"score": 0.0, "derivative": 0.0, "integrated": 0.0}

        length_signal = min(1.0, len(response) / 1000.0)
        diversity_signal = len(set(response.split())) / max(len(response.split()), 1)
        structure_signal = min(1.0, response.count("\n") / 10.0)
        raw_score = length_signal * 0.3 + diversity_signal * 0.4 + structure_signal * 0.3

        derivative = raw_score - damping * prev_score
        integrated = prev_score + derivative * 0.5
        score = max(0.0, min(1.0, integrated))

        self.stats["avg_score"] = round(
            (self.stats["avg_score"] * (self.stats["scores_computed"] - 1) + score) / self.stats["scores_computed"], 4,
        )
        self.score_history.append(score)

        return {
            "score": round(score, 4), "derivative": round(derivative, 4),
            "integrated": round(integrated, 4), "raw_signal": round(raw_score, 4),
        }

    def get_stats(self) -> dict:
        return self.stats
