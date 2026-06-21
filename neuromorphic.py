"""
Ketchum's Physics Optimized Super Intelligence
Neuromorphic Spike Classifier — v2

PHYSICS:
- Inhibitory connections: competing intents suppress each other
- Temporal coding: word ORDER matters (earlier spikes weighted more)
- Refractory period: neurons can't re-fire immediately
- Adaptive threshold: frequently-firing neurons raise threshold
- STDP with exponential forgetting curve
"""

import math
import time
from typing import Optional
from collections import defaultdict


class NeuromorphicSpikeClassifier:

    INHIBITORY = {
        "coding": ["creative", "general"],
        "creative": ["coding", "math"],
        "math": ["creative", "general"],
        "research": ["creative"],
        "reasoning": ["general"],
        "planning": ["general"],
        "analysis": ["creative", "general"],
        "general": [],
    }

    def __init__(self):
        self.base_threshold = 1.0
        self.reset_value = 0.0
        self.leak_rate = 0.03
        self.refractory_steps = 3
        self.adaptation_rate = 0.1

        self.neurons = {
            name: {"potential": 0.0, "spikes": 0, "last_spike": -100,
                   "threshold": self.base_threshold, "adaptation": 0.0}
            for name in ["coding", "reasoning", "research", "creative",
                         "math", "planning", "analysis", "general"]
        }

        self.synaptic_weights = {
            "coding": {
                "code": 0.8, "function": 0.7, "debug": 0.6,
                "python": 0.8, "javascript": 0.7, "build": 0.5,
                "api": 0.6, "class": 0.6, "program": 0.7,
                "script": 0.6, "variable": 0.5, "loop": 0.5,
                "compile": 0.7, "runtime": 0.5, "syntax": 0.6,
                "import": 0.5, "module": 0.5, "library": 0.4,
            },
            "reasoning": {
                "why": 0.8, "explain": 0.7, "because": 0.5,
                "how": 0.6, "understand": 0.6, "logic": 0.7,
                "reason": 0.7, "think": 0.5, "analyze": 0.4,
                "therefore": 0.7, "however": 0.5, "thus": 0.6,
                "since": 0.5, "conclude": 0.6, "infer": 0.5,
            },
            "research": {
                "research": 0.9, "find": 0.6, "search": 0.6,
                "latest": 0.7, "discover": 0.6, "study": 0.6,
                "evidence": 0.5, "data": 0.5, "source": 0.5,
                "paper": 0.7, "publication": 0.6, "survey": 0.5,
                "literature": 0.6, "experiment": 0.5,
            },
            "creative": {
                "write": 0.7, "story": 0.9, "creative": 0.8,
                "poem": 0.9, "imagine": 0.7, "design": 0.5,
                "invent": 0.6, "fiction": 0.8, "art": 0.6,
                "novel": 0.7, "character": 0.6, "narrative": 0.7,
                "compose": 0.6, "lyrics": 0.7,
            },
            "math": {
                "calculate": 0.9, "solve": 0.8, "equation": 0.9,
                "formula": 0.8, "math": 0.9, "number": 0.6,
                "algebra": 0.7, "integral": 0.8, "derivative": 0.8,
                "theorem": 0.7, "proof": 0.7, "compute": 0.6,
                "polynomial": 0.7, "matrix": 0.7, "vector": 0.6,
            },
            "planning": {
                "plan": 0.9, "strategy": 0.8, "steps": 0.7,
                "roadmap": 0.8, "schedule": 0.7, "goal": 0.6,
                "milestone": 0.6, "timeline": 0.7, "organize": 0.6,
                "prioritize": 0.7, "delegate": 0.5, "deadline": 0.6,
                "phase": 0.6, "objective": 0.6,
            },
            "analysis": {
                "analyze": 0.9, "review": 0.7, "evaluate": 0.7,
                "compare": 0.7, "assess": 0.7, "measure": 0.6,
                "report": 0.5, "insight": 0.6, "trend": 0.6,
                "benchmark": 0.6, "metric": 0.6, "score": 0.5,
                "ratio": 0.5, "statistic": 0.6, "correlation": 0.6,
            },
            "general": {
                "help": 0.4, "tell": 0.3, "what": 0.3,
                "show": 0.3, "give": 0.3, "make": 0.3,
                "please": 0.2, "thanks": 0.1, "hello": 0.2,
            },
        }

        self.classification_log = []
        self.stdp_updates = 0
        self.stdp_learning_rate = 0.01

    def classify(self, prompt: str) -> dict:
        start_time = time.time()
        words = prompt.lower().split()

        for name in self.neurons:
            self.neurons[name]["potential"] = 0.0
            self.neurons[name]["spikes"] = 0
            self.neurons[name]["last_spike"] = -100
            self.neurons[name]["adaptation"] *= 0.5
            self.neurons[name]["threshold"] = self.base_threshold + self.neurons[name]["adaptation"]

        spike_record = []
        inhibition_events = 0

        for step, word in enumerate(words):
            word_clean = word.strip(".,!?;:()[]")

            for name in self.neurons:
                self.neurons[name]["potential"] -= self.leak_rate
                self.neurons[name]["potential"] = max(0.0, self.neurons[name]["potential"])

            fired_this_step = []

            for neuron_name, weights in self.synaptic_weights.items():
                if word_clean not in weights:
                    continue
                neuron = self.neurons[neuron_name]

                if step - neuron["last_spike"] < self.refractory_steps:
                    continue

                temporal_weight = math.exp(-0.03 * step)
                neuron["potential"] += weights[word_clean] * (0.5 + 0.5 * temporal_weight)

                if neuron["potential"] >= neuron["threshold"]:
                    neuron["spikes"] += 1
                    neuron["last_spike"] = step
                    temporal_score = 1.0 / (1.0 + 0.1 * step)

                    spike_record.append({
                        "neuron": neuron_name, "step": step,
                        "word": word_clean, "temporal_score": round(temporal_score, 4),
                    })

                    neuron["potential"] = self.reset_value
                    neuron["adaptation"] += self.adaptation_rate * 0.1
                    neuron["threshold"] = self.base_threshold + neuron["adaptation"]
                    fired_this_step.append(neuron_name)

            for fired_neuron in fired_this_step:
                if fired_neuron in self.INHIBITORY:
                    for suppressed in self.INHIBITORY[fired_neuron]:
                        if suppressed in self.neurons:
                            self.neurons[suppressed]["potential"] -= 0.15
                            self.neurons[suppressed]["potential"] = max(
                                0.0, self.neurons[suppressed]["potential"]
                            )
                            inhibition_events += 1

        total_spikes = sum(n["spikes"] for n in self.neurons.values())

        if total_spikes == 0:
            winner = "general"
            max_potential = 0.0
            for name, neuron in self.neurons.items():
                if neuron["potential"] > max_potential:
                    max_potential = neuron["potential"]
                    winner = name
            confidence = 0.0
        else:
            weighted_scores = {}
            for spike in spike_record:
                neuron = spike["neuron"]
                temporal = spike["temporal_score"]
                weighted_scores[neuron] = weighted_scores.get(neuron, 0) + temporal
            for name, neuron in self.neurons.items():
                base_score = neuron["spikes"] * 0.5
                weighted_scores[name] = weighted_scores.get(name, 0) + base_score
            winner = max(weighted_scores, key=weighted_scores.get)
            winner_score = weighted_scores[winner]
            total_score = sum(weighted_scores.values())
            confidence = winner_score / total_score if total_score > 0 else 0.0

        classification_time_ms = (time.time() - start_time) * 1000

        result = {
            "intent": winner, "confidence": round(confidence, 4),
            "total_spikes": total_spikes, "winner_spikes": self.neurons[winner]["spikes"],
            "spike_record": spike_record[:30], "inhibition_events": inhibition_events,
            "classification_ms": round(classification_time_ms, 3),
            "all_neurons": {
                name: {
                    "spikes": n["spikes"], "potential": round(n["potential"], 4),
                    "adaptation": round(n["adaptation"], 4), "threshold": round(n["threshold"], 4),
                }
                for name, n in self.neurons.items()
            },
        }
        self.classification_log.append(result)
        return result

    def stdp_learn(self, intent: str, prompt: str, was_correct: bool):
        words = prompt.lower().split()
        effective_rate = self.stdp_learning_rate * math.exp(-0.001 * self.stdp_updates)
        effective_rate = max(effective_rate, 0.001)
        for word in words:
            word_clean = word.strip(".,!?;:()[]")
            if intent in self.synaptic_weights:
                weights = self.synaptic_weights[intent]
                if word_clean in weights:
                    if was_correct:
                        weights[word_clean] = min(1.0, weights[word_clean] + effective_rate)
                    else:
                        weights[word_clean] = max(0.0, weights[word_clean] - effective_rate)
        self.stdp_updates += 1

    def get_stats(self) -> dict:
        if not self.classification_log:
            return {"classifications": 0}
        avg_time = sum(c["classification_ms"] for c in self.classification_log) / len(self.classification_log)
        avg_confidence = sum(c["confidence"] for c in self.classification_log) / len(self.classification_log)
        avg_inhibition = sum(c.get("inhibition_events", 0) for c in self.classification_log) / len(self.classification_log)
        return {
            "total_classifications": len(self.classification_log),
            "avg_classification_ms": round(avg_time, 3),
            "avg_confidence": round(avg_confidence, 4),
            "avg_inhibition_events": round(avg_inhibition, 2),
            "stdp_updates": self.stdp_updates,
            "effective_learning_rate": round(
                self.stdp_learning_rate * math.exp(-0.001 * self.stdp_updates), 6
            ),
        }
