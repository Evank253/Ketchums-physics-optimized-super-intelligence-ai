"""
Ketchum's Physics Optimized Super Intelligence
Information Field Optimizer — v2

PHYSICS:
- Compression-based entropy (Li et al. 2004): gzip length as entropy proxy
- Mutual information: C(X) + C(Y) - C(X,Y)
- KL divergence for distribution alignment
- Compression-cost per sentence for information density
- Signal-to-noise via compression gap
"""

import math
import zlib
from collections import Counter
from typing import Optional


class InformationFieldOptimizer:

    def __init__(self):
        self.channel_capacities = {
            "coding": 8.0, "reasoning": 6.0, "research": 7.0,
            "creative": 5.0, "math": 9.0, "planning": 6.5,
            "analysis": 7.0, "general": 4.0,
        }
        self.stats = {
            "entropy_calculations": 0, "snr_calculations": 0,
            "mi_calculations": 0, "avg_entropy": 0.0, "avg_snr": 0.0,
        }

    def calculate_shannon_entropy(self, text: str) -> float:
        self.stats["entropy_calculations"] += 1
        if not text:
            return 0.0

        raw_bytes = text.encode("utf-8")
        compressed = zlib.compress(raw_bytes, level=6)
        compression_ratio = len(compressed) / max(len(raw_bytes), 1)
        entropy_bits = compression_ratio * 8

        words = text.lower().split()
        if len(words) > 1:
            word_counts = Counter(words)
            total = len(words)
            word_entropy = -sum((c / total) * math.log2(c / total) for c in word_counts.values())
            alpha = min(1.0, len(words) / 100.0)
            entropy = (1 - alpha) * entropy_bits + alpha * word_entropy
        else:
            entropy = entropy_bits

        self.stats["avg_entropy"] = round(
            (self.stats["avg_entropy"] * (self.stats["entropy_calculations"] - 1) + entropy)
            / self.stats["entropy_calculations"], 4,
        )
        return round(entropy, 4)

    def calculate_signal_to_noise(self, text: str) -> dict:
        self.stats["snr_calculations"] += 1
        if not text:
            return {"signal_to_noise": 0.0, "signal": 0.0, "noise": 0.0}

        words = text.lower().split()
        total_words = len(words)
        if total_words == 0:
            return {"signal_to_noise": 0.0, "signal": 0.0, "noise": 0.0}

        full_compressed = len(zlib.compress(text.encode("utf-8"), 6))
        unique_text = " ".join(set(words))
        unique_compressed = len(zlib.compress(unique_text.encode("utf-8"), 6))

        signal = unique_compressed
        noise = max(0, full_compressed - unique_compressed)
        snr = signal / max(noise, 1)

        filler_words = {
            "the", "a", "an", "is", "are", "was", "were", "be",
            "been", "being", "have", "has", "had", "do", "does",
            "did", "will", "would", "could", "should", "may",
            "might", "can", "shall", "to", "of", "in", "for",
            "on", "with", "at", "by", "from", "as", "into",
        }
        filler_ratio = sum(1 for w in words if w in filler_words) / total_words

        self.stats["avg_snr"] = round(
            (self.stats["avg_snr"] * (self.stats["snr_calculations"] - 1) + snr)
            / self.stats["snr_calculations"], 4,
        )
        return {
            "signal_to_noise": round(snr, 4), "signal_bytes": signal,
            "noise_bytes": noise, "total_words": total_words,
            "unique_words": len(set(words)),
            "unique_ratio": round(len(set(words)) / total_words, 4),
            "filler_ratio": round(filler_ratio, 4),
        }

    def calculate_mutual_information(self, prompt: str, response: str) -> float:
        self.stats["mi_calculations"] += 1
        if not prompt or not response:
            return 0.0

        c_prompt = len(zlib.compress(prompt.encode("utf-8"), 6))
        c_response = len(zlib.compress(response.encode("utf-8"), 6))
        c_joint = len(zlib.compress((prompt + " " + response).encode("utf-8"), 6))

        mi_compressed = c_prompt + c_response - c_joint
        normalizer = min(c_prompt, c_response)
        mi_normalized = max(0.0, min(1.0, mi_compressed / normalizer)) if normalizer > 0 else 0.0
        return round(mi_normalized, 4)

    def calculate_kl_divergence(self, prompt: str, response: str) -> float:
        if not prompt or not response:
            return float("inf")
        prompt_words = prompt.lower().split()
        response_words = response.lower().split()
        if not prompt_words or not response_words:
            return float("inf")

        prompt_counts = Counter(prompt_words)
        response_counts = Counter(response_words)
        vocab = set(prompt_counts.keys()) | set(response_counts.keys())

        alpha = 0.1
        prompt_total = len(prompt_words) + alpha * len(vocab)
        response_total = len(response_words) + alpha * len(vocab)

        kl = 0.0
        for word in vocab:
            p = (prompt_counts.get(word, 0) + alpha) / prompt_total
            q = (response_counts.get(word, 0) + alpha) / response_total
            kl += p * math.log2(p / q)
        return round(kl, 4)

    def get_channel_capacity(self, query_type: str) -> dict:
        capacity = self.channel_capacities.get(query_type, 4.0)
        return {
            "query_type": query_type, "capacity_bits": capacity,
            "capacity_category": "high" if capacity >= 7.0 else "medium" if capacity >= 5.0 else "low",
        }

    def maximize_information_density(self, text: str) -> str:
        if not text or len(text) < 50:
            return text
        sentences = [s.strip() for s in text.split(". ") if s.strip()]
        if len(sentences) <= 2:
            return text

        scored = []
        for sentence in sentences:
            if not sentence:
                continue
            s_compressed = len(zlib.compress(sentence.encode("utf-8"), 6))
            info_density = s_compressed / max(len(sentence), 1)
            scored.append((sentence, info_density))

        if not scored:
            return text

        densities = [d for _, d in scored]
        median_density = sorted(densities)[len(densities) // 2]
        kept = [s for s, d in scored if d >= median_density * 0.7]
        if not kept:
            kept = [s for s, _ in scored[:max(2, len(scored) * 2 // 3)]]

        original_order = [s for s in sentences if s in kept]
        if not original_order:
            original_order = kept
        return ". ".join(original_order)

    def get_stats(self) -> dict:
        return {**self.stats, "channel_types": len(self.channel_capacities)}
