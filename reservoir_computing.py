"""
Ketchum's Physics Optimized Super Intelligence
Reservoir Computing Aggregator — v2

PHYSICS:
- Echo state property: fading memory of recent inputs
- Edge of chaos: spectral radius near 1.0 for rich dynamics
- Trainable readout via ridge regression (only output layer trained)
- Separation metric: measures how well reservoir discriminates inputs
- Auto-training from accumulated quality feedback
"""

import numpy as np
import math
from typing import Optional
from collections import defaultdict


class ReservoirComputingAggregator:

    def __init__(self, reservoir_size: int = 100, spectral_radius: float = 0.95,
                 input_scaling: float = 0.5, leak_rate: float = 0.3,
                 washout: int = 5, ridge_alpha: float = 1e-4):
        self.reservoir_size = reservoir_size
        self.spectral_radius = spectral_radius
        self.input_scaling = input_scaling
        self.leak_rate = leak_rate
        self.washout = washout
        self.ridge_alpha = ridge_alpha

        np.random.seed(42)
        W = np.random.randn(reservoir_size, reservoir_size) * 0.1
        eigenvalues = np.abs(np.linalg.eigvals(W))
        max_eigenvalue = np.max(eigenvalues)
        if max_eigenvalue > 0:
            W = W * (spectral_radius / max_eigenvalue)

        self.W_reservoir = W
        self.W_input = np.random.randn(reservoir_size, reservoir_size) * 0.1
        self.state = np.zeros(reservoir_size)

        self.W_readout = None
        self.is_trained = False
        self.training_states = []
        self.training_labels = []
        self.processing_log = []

    def _encode_response(self, response: str) -> np.ndarray:
        vec = np.zeros(self.reservoir_size)
        if not response:
            return vec
        for i, char in enumerate(response[:self.reservoir_size]):
            vec[i % self.reservoir_size] += ord(char) / 128.0
        words = response.lower().split()
        for i, word in enumerate(words[:self.reservoir_size // 4]):
            idx = hash(word) % self.reservoir_size
            vec[idx] += 1.0 / max(len(words), 1)
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec

    def _state_entropy(self, state: np.ndarray) -> float:
        abs_state = np.abs(state)
        total = np.sum(abs_state)
        if total == 0:
            return 0.0
        probs = abs_state / total
        return -sum(p * math.log2(p) for p in probs if p > 1e-10)

    def _collect_states(self, responses: list) -> list:
        self.state = np.zeros(self.reservoir_size)
        all_states = []
        for response in responses:
            input_vec = self._encode_response(response)
            for _ in range(3):
                pre_activation = (
                    self.W_reservoir @ self.state
                    + self.W_input @ input_vec * self.input_scaling
                )
                self.state = (1.0 - self.leak_rate) * self.state + self.leak_rate * np.tanh(pre_activation)
            all_states.append(self.state.copy())
        return all_states

    def measure_separation(self, states: list) -> float:
        if len(states) < 2:
            return 0.0
        distances = [np.linalg.norm(states[i] - states[j]) for i in range(len(states)) for j in range(i + 1, len(states))]
        if not distances:
            return 0.0
        mean_dist = np.mean(distances)
        std_dist = np.std(distances) if len(distances) > 1 else 0.0
        return min(mean_dist / (std_dist + 1e-10), 100.0)

    def train_readout(self, responses: list, quality_labels: list):
        if len(responses) != len(quality_labels) or len(responses) < 2:
            return
        states = self._collect_states(responses)
        X = np.array(states)
        Y = np.array(quality_labels).reshape(-1, 1)
        XtX = X.T @ X + self.ridge_alpha * np.eye(self.reservoir_size)
        try:
            self.W_readout = (Y.T @ X @ np.linalg.inv(XtX)).reshape(1, -1)
            self.is_trained = True
        except np.linalg.LinAlgError:
            self.W_readout = (Y.T @ np.linalg.pinv(X)).reshape(1, -1)
            self.is_trained = True

    def process_responses(self, responses: list, query_type: str) -> dict:
        if not responses:
            return {"best": "", "method": "empty"}
        if len(responses) == 1:
            return {"best": responses[0], "method": "single", "reservoir_used": False}

        states = self._collect_states(responses)
        separation = self.measure_separation(states)
        scores = []

        if self.is_trained and self.W_readout is not None:
            for state in states:
                predicted_quality = float(self.W_readout @ state)
                energy = np.sum(state ** 2)
                entropy = self._state_entropy(state)
                energy_score = energy * 0.6 + entropy * 0.4
                scores.append(0.7 * predicted_quality + 0.3 * energy_score)
            method = "trained_readout"
        else:
            for state in states:
                energy = np.sum(state ** 2)
                entropy = self._state_entropy(state)
                scores.append(energy * 0.6 + entropy * 0.4)
            method = "energy_heuristic"

        best_idx = int(np.argmax(scores))
        self.processing_log.append({
            "responses_count": len(responses), "scores": [round(s, 4) for s in scores],
            "best_idx": best_idx, "query_type": query_type,
            "method": method, "separation": round(separation, 4), "is_trained": self.is_trained,
        })

        return {
            "best": responses[best_idx], "best_score": round(scores[best_idx], 4),
            "all_scores": [round(s, 4) for s in scores], "reservoir_used": True,
            "method": method, "separation": round(separation, 4), "is_trained": self.is_trained,
            "reservoir_state_energy": round(float(np.sum(self.state ** 2)), 4),
        }

    def add_training_example(self, response: str, quality: float):
        states = self._collect_states([response])
        self.training_states.append(states[0])
        self.training_labels.append(quality)
        if len(self.training_states) >= 10 and len(self.training_states) % 5 == 0:
            self.train_readout_from_accumulated()

    def train_readout_from_accumulated(self):
        if len(self.training_states) < 5:
            return
        X = np.array(self.training_states)
        Y = np.array(self.training_labels).reshape(-1, 1)
        XtX = X.T @ X + self.ridge_alpha * np.eye(self.reservoir_size)
        try:
            self.W_readout = (Y.T @ X @ np.linalg.inv(XtX)).reshape(1, -1)
            self.is_trained = True
        except np.linalg.LinAlgError:
            self.W_readout = (Y.T @ np.linalg.pinv(X)).reshape(1, -1)
            self.is_trained = True

    def get_stats(self) -> dict:
        if not self.processing_log:
            return {"processes": 0, "is_trained": self.is_trained}
        method_counts = defaultdict(int)
        for p in self.processing_log:
            method_counts[p.get("method", "unknown")] += 1
        return {
            "total_processes": len(self.processing_log),
            "avg_responses": round(sum(p["responses_count"] for p in self.processing_log) / len(self.processing_log), 2),
            "reservoir_size": self.reservoir_size, "spectral_radius": self.spectral_radius,
            "is_trained": self.is_trained, "training_examples": len(self.training_states),
            "avg_separation": round(sum(p.get("separation", 0) for p in self.processing_log) / len(self.processing_log), 4),
            "method_distribution": dict(method_counts),
        }
