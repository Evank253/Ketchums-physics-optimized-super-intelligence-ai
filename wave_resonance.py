"""
Ketchum's Physics Optimized Super Intelligence
Wave Resonance Engine — v2

PHYSICS:
- Cross-spectral density between prompt and response signals
- Coherence: |S_xy|^2 / (S_xx * S_yy)
- Phase consistency from circular mean
- Peak cross-correlation for time-domain alignment
"""

import numpy as np
from typing import Optional


class WaveResonanceEngine:

    def __init__(self, resonance_threshold: float = 0.5):
        self.resonance_threshold = resonance_threshold
        self.resonance_log = []
        self.stats = {"calculations": 0, "avg_resonance": 0.0, "in_resonance_count": 0}

    def _text_to_signal(self, text: str) -> np.ndarray:
        if not text:
            return np.array([0.0])
        signal = np.array([ord(c) for c in text], dtype=np.float64)
        mean = np.mean(signal)
        std = np.std(signal)
        return (signal - mean) / std if std > 0 else signal - mean

    def calculate_resonance(self, prompt: str, response: str, query_type: str) -> dict:
        self.stats["calculations"] += 1

        prompt_signal = self._text_to_signal(prompt)
        response_signal = self._text_to_signal(response)

        min_length = 16
        if len(prompt_signal) < min_length or len(response_signal) < min_length:
            return self._simple_resonance(prompt, response, query_type)

        max_len = max(len(prompt_signal), len(response_signal))
        fft_len = 1
        while fft_len < max_len:
            fft_len *= 2

        prompt_padded = np.zeros(fft_len)
        response_padded = np.zeros(fft_len)
        prompt_padded[:len(prompt_signal)] = prompt_signal
        response_padded[:len(response_signal)] = response_signal

        prompt_fft = np.fft.fft(prompt_padded)
        response_fft = np.fft.fft(response_padded)
        prompt_power = np.abs(prompt_fft) ** 2
        response_power = np.abs(response_fft) ** 2

        cross_spectrum = prompt_fft * np.conj(response_fft)
        cross_power = np.abs(cross_spectrum)

        coherence_denom = prompt_power * response_power
        coherence = np.where(coherence_denom > 1e-10, cross_power ** 2 / coherence_denom, 0.0)
        mean_coherence = float(np.mean(coherence[1:len(coherence) // 2])) if len(coherence) > 1 else 0.0

        correlation = np.correlate(prompt_padded, response_padded, mode="full")
        norm = np.sqrt(np.sum(prompt_padded ** 2) * np.sum(response_padded ** 2))
        if norm > 0:
            correlation = correlation / norm
        peak_correlation = float(np.max(np.abs(correlation)))

        phase_diff = np.angle(cross_spectrum[1:len(cross_spectrum) // 2])
        mean_cos = np.mean(np.cos(phase_diff))
        mean_sin = np.mean(np.sin(phase_diff))
        phase_consistency = float(np.sqrt(mean_cos ** 2 + mean_sin ** 2))

        resonance_score = min(1.0, mean_coherence * 0.4 + peak_correlation * 0.35 + phase_consistency * 0.25)
        in_resonance = resonance_score >= self.resonance_threshold

        constructive = mean_coherence * phase_consistency
        destructive = mean_coherence * (1.0 - phase_consistency)

        self.stats["avg_resonance"] = round(
            (self.stats["avg_resonance"] * (self.stats["calculations"] - 1) + resonance_score)
            / self.stats["calculations"], 4,
        )
        if in_resonance:
            self.stats["in_resonance_count"] += 1

        result = {
            "resonance_score": round(resonance_score, 4), "in_resonance": in_resonance,
            "mean_coherence": round(mean_coherence, 4), "peak_correlation": round(peak_correlation, 4),
            "phase_consistency": round(phase_consistency, 4),
            "constructive": round(float(constructive), 4), "destructive": round(float(destructive), 4),
            "query_type": query_type,
        }
        self.resonance_log.append(result)
        return result

    def _simple_resonance(self, prompt: str, response: str, query_type: str) -> dict:
        pw = set(prompt.lower().split())
        rw = set(response.lower().split())
        jaccard = len(pw & rw) / max(len(pw | rw), 1)
        return {
            "resonance_score": round(jaccard, 4), "in_resonance": jaccard >= self.resonance_threshold,
            "mean_coherence": round(jaccard, 4), "peak_correlation": round(jaccard, 4),
            "phase_consistency": 0.0, "constructive": round(jaccard, 4), "destructive": 0.0,
            "query_type": query_type,
        }

    def tune_response(self, response: str, resonance: dict, query_type: str) -> str:
        if resonance["in_resonance"]:
            return response
        sentences = [s.strip() for s in response.split(". ") if s.strip()]
        if len(sentences) <= 1:
            return response
        scored = [(s, self.calculate_resonance("", s, query_type)["resonance_score"]) for s in sentences]
        scored.sort(key=lambda x: x[1], reverse=True)
        keep_count = max(2, int(len(scored) * 0.8))
        kept_set = {s for s, _ in scored[:keep_count]}
        result_sentences = [s for s in sentences if s in kept_set]
        if not result_sentences:
            result_sentences = list(kept_set)
        return ". ".join(result_sentences)

    def get_resonance_stats(self) -> dict:
        resonance_rate = self.stats["in_resonance_count"] / max(self.stats["calculations"], 1)
        return {**self.stats, "resonance_rate": round(resonance_rate, 4), "resonance_threshold": self.resonance_threshold}
