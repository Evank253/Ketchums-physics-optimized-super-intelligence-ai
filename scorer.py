"""
Ketchum's Physics Optimized Super Intelligence
Response Scorer — v2
"""

import math
from typing import Optional
from collections import Counter


def score_response(response: str, query_type: str) -> float:
    if not response:
        return 0.0
    score = 0.0
    length = len(response)
    if length < 10: score += 0.0
    elif length < 50: score += 1.0
    elif length < 200: score += 2.0
    elif length < 2000: score += 3.0
    else: score += 2.5

    words = response.lower().split()
    if words:
        unique_ratio = len(set(words)) / len(words)
        score += min(3.0, unique_ratio * 4.0)

    if "```" in response: score += 1.0
    if any(marker in response for marker in ["1.", "2.", "3."]): score += 1.0
    if "\n\n" in response: score += 0.5

    type_keywords = {
        "coding": ["code", "function", "def", "class", "import", "return"],
        "reasoning": ["because", "therefore", "however", "since", "thus"],
        "research": ["study", "evidence", "according", "data", "found"],
        "creative": ["imagine", "story", "once", "dream", "wonder"],
        "math": ["equation", "solve", "=", "formula", "calculate"],
        "planning": ["step", "first", "then", "next", "finally"],
        "analysis": ["compare", "contrast", "evaluate", "assess", "versus"],
        "general": [],
    }
    keywords = type_keywords.get(query_type, [])
    if keywords:
        matches = sum(1 for k in keywords if k in response.lower())
        score += min(2.0, matches * 0.5)
    else:
        score += 1.0

    return round(min(score, 10.0), 2)


def pick_best_response(responses: list, query_type: str = "general") -> str:
    if not responses:
        return ""
    if len(responses) == 1:
        return responses[0]
    scored = [(r, score_response(r, query_type)) for r in responses]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[0][0]
