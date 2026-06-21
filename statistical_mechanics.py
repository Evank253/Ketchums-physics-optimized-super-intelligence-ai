"""
Ketchum's Physics Optimized Super Intelligence
Statistical Mechanics Optimizer — v2

PHYSICS:
- Boltzmann distribution: P(state) ~ exp(-E/kT)
- Simulated annealing with cooling schedule
- Partition function normalization
- Energy states learned from quality feedback
"""

import math
import random
from typing import Optional
from collections import defaultdict


class StatisticalMechanicsOptimizer:

    def __init__(self, temperature: float = 1.0, cooling_rate: float = 0.95):
        self.temperature = temperature
        self.cooling_rate = cooling_rate
        self.min_temperature = 0.1

        self.energy_states = {
            "gpt-4-turbo": {"coding": 0.5, "reasoning": 0.8, "research": 0.7,
                             "creative": 0.6, "math": 0.7, "planning": 0.8,
                             "analysis": 0.6, "general": 0.5},
            "claude-3-opus": {"coding": 0.7, "reasoning": 0.5, "research": 0.6,
                              "creative": 0.5, "math": 0.8, "planning": 0.6,
                              "analysis": 0.5, "general": 0.4},
            "claude-3-sonnet": {"coding": 0.6, "reasoning": 0.7, "research": 0.5,
                                "creative": 0.7, "math": 0.6, "planning": 0.7,
                                "analysis": 0.6, "general": 0.5},
            "gemini-pro": {"coding": 0.8, "reasoning": 0.6, "research": 0.4,
                           "creative": 0.6, "math": 0.5, "planning": 0.8,
                           "analysis": 0.7, "general": 0.6},
            "mistral-local": {"coding": 0.6, "reasoning": 0.9, "research": 0.8,
                               "creative": 0.9, "math": 0.9, "planning": 0.9,
                               "analysis": 0.8, "general": 0.7},
        }

        self.selection_log = []
        self.stats = {"selections": 0, "avg_temperature": temperature}

    def boltzmann_select(self, models: list, query_type: str) -> dict:
        self.stats["selections"] += 1
        energies = {model: self.energy_states.get(model, {}).get(query_type, 1.0) for model in models}

        boltzmann_weights = {
            model: math.exp(-energy / max(self.temperature, 0.01))
            for model, energy in energies.items()
        }
        Z = sum(boltzmann_weights.values())
        probabilities = {model: w / Z for model, w in boltzmann_weights.items()}

        r = random.random()
        cumulative = 0.0
        selected = models[0] if models else "gpt-4-turbo"
        for model, prob in sorted(probabilities.items(), key=lambda x: -x[1]):
            cumulative += prob
            if r <= cumulative:
                selected = model
                break

        self.temperature = max(self.min_temperature, self.temperature * self.cooling_rate)
        self.stats["avg_temperature"] = round(
            (self.stats["avg_temperature"] * (self.stats["selections"] - 1) + self.temperature)
            / self.stats["selections"], 4,
        )

        result = {
            "selected": selected,
            "probability": round(probabilities.get(selected, 0.0), 6),
            "temperature": round(self.temperature, 4),
            "all_probabilities": {k: round(v, 6) for k, v in probabilities.items()},
            "energies": energies,
        }
        self.selection_log.append(result)
        return result

    def update_model_energy(self, model: str, quality: float, query_type: str):
        if model not in self.energy_states:
            self.energy_states[model] = {}
        if query_type not in self.energy_states[model]:
            self.energy_states[model][query_type] = 1.0
        new_energy = 1.0 / max(quality, 0.1) if quality > 0 else 2.0
        current = self.energy_states[model][query_type]
        self.energy_states[model][query_type] = 0.7 * current + 0.3 * new_energy

    def get_stats(self) -> dict:
        return {
            **self.stats,
            "current_temperature": round(self.temperature, 4),
            "models_tracked": len(self.energy_states),
        }
