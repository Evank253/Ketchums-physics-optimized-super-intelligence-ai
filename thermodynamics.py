"""
Ketchum's Physics Optimized Super Intelligence
Thermodynamic Engine — v2

PHYSICS:
- Carnot efficiency: eta = 1 - T_cold/T_hot
- Real power estimation via psutil
- Energy-proportional model routing
- Joule-per-query tracking per model
"""

import math
import time
from typing import Optional
from collections import defaultdict

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


class ThermodynamicEngine:

    KB = 1.380649e-23
    MODEL_POWER = {
        "gpt-4-turbo": 50.0, "claude-3-opus": 45.0,
        "claude-3-sonnet": 20.0, "gemini-pro": 40.0, "mistral-local": 5.0,
    }
    IDLE_POWER_W = 30.0
    PER_CORE_POWER_W = 10.0

    def __init__(self):
        self.T_hot = 600
        self.T_cold = 300
        self.carnot_efficiency = 1.0 - (self.T_cold / self.T_hot)
        self.query_energy_log = []
        self.thermal_history = []
        self.stats = {
            "thermal_routes": 0, "avg_efficiency": 0.0, "total_entropy": 0.0,
            "total_joules": 0.0, "avg_joules_per_query": 0.0,
            "state_distribution": {"COLD": 0, "WARM": 0, "HOT": 0, "CRITICAL": 0},
        }

    def measure_system_power(self) -> dict:
        if HAS_PSUTIL:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_count = psutil.cpu_count(logical=True) or 4
            memory_percent = psutil.virtual_memory().percent
            active_cores = (cpu_percent / 100.0) * cpu_count
            cpu_power = self.IDLE_POWER_W + active_cores * self.PER_CORE_POWER_W
            mem_power = (memory_percent / 100.0) * 10.0
            total_power = cpu_power + mem_power
        else:
            cpu_percent = 30.0
            total_power = self.IDLE_POWER_W + 2 * self.PER_CORE_POWER_W

        return {
            "estimated_power_w": round(total_power, 2), "cpu_percent": round(cpu_percent, 1),
            "method": "psutil" if HAS_PSUTIL else "estimated",
        }

    def get_thermal_state(self, cpu_load: float) -> dict:
        if cpu_load < 0.3:
            state, temperature = "COLD", self.T_cold + (cpu_load / 0.3) * 100
        elif cpu_load < 0.6:
            state, temperature = "WARM", 400 + ((cpu_load - 0.3) / 0.3) * 100
        elif cpu_load < 0.85:
            state, temperature = "HOT", 500 + ((cpu_load - 0.6) / 0.25) * 80
        else:
            state, temperature = "CRITICAL", 580 + ((cpu_load - 0.85) / 0.15) * 50

        efficiency = 1.0 - (self.T_cold / max(temperature, self.T_cold + 1))
        return {
            "state": state, "temperature_K": round(temperature, 1),
            "efficiency": round(efficiency, 4), "carnot_limit": round(self.carnot_efficiency, 4),
            "cpu_load": round(cpu_load, 4),
        }

    def route_by_thermal_state(self, query_type: str, cpu_load: float) -> dict:
        self.stats["thermal_routes"] += 1
        thermal = self.get_thermal_state(cpu_load)
        self.stats["state_distribution"][thermal["state"]] += 1
        power = self.measure_system_power()

        model_recommendations = {
            "COLD": {"primary": "gpt-4-turbo", "reason": "Low load — energy is cheap", "energy_budget_j": 2.0},
            "WARM": {"primary": "claude-3-opus", "reason": "Moderate load — balanced", "energy_budget_j": 1.0},
            "HOT": {"primary": "claude-3-sonnet", "reason": "High load — efficient model", "energy_budget_j": 0.5},
            "CRITICAL": {"primary": "mistral-local", "reason": "Critical load — minimize energy", "energy_budget_j": 0.1},
        }

        recommendation = model_recommendations.get(thermal["state"], model_recommendations["WARM"])
        model_power = self.MODEL_POWER.get(recommendation["primary"], 30.0)
        estimated_energy_j = model_power * 0.5
        budget = recommendation["energy_budget_j"]

        if estimated_energy_j > budget:
            for fallback in ["claude-3-sonnet", "mistral-local"]:
                fallback_energy = self.MODEL_POWER.get(fallback, 30.0) * 0.5
                if fallback_energy <= budget:
                    recommendation["primary"] = fallback
                    recommendation["reason"] += " (downgraded: energy budget exceeded)"
                    estimated_energy_j = fallback_energy
                    break

        self.stats["avg_efficiency"] = round(
            (self.stats["avg_efficiency"] * (self.stats["thermal_routes"] - 1) + thermal["efficiency"])
            / self.stats["thermal_routes"], 4,
        )

        return {
            "thermal": thermal, "power": power, "recommendation": recommendation,
            "efficiency": thermal["efficiency"], "estimated_energy_j": round(estimated_energy_j, 4),
        }

    def track_query_energy(self, model: str, latency_ms: float, query_type: str) -> dict:
        model_power = self.MODEL_POWER.get(model, 30.0)
        system_power = self.measure_system_power()
        query_time_s = latency_ms / 1000.0
        model_energy = model_power * query_time_s
        system_energy = system_power["estimated_power_w"] * query_time_s
        total_joules = model_energy + system_energy

        self.stats["total_joules"] += total_joules
        self.query_energy_log.append({
            "model": model, "joules": total_joules, "latency_ms": latency_ms, "query_type": query_type,
        })
        self.stats["avg_joules_per_query"] = round(self.stats["total_joules"] / len(self.query_energy_log), 6)

        return {
            "total_joules": round(total_joules, 6), "model_joules": round(model_energy, 6),
            "system_joules": round(system_energy, 6), "model_power_w": model_power,
            "system_power_w": system_power["estimated_power_w"],
            "efficiency_j_per_ms": round(total_joules / max(latency_ms, 1), 6),
        }

    def calculate_entropy(self, text: str) -> float:
        if not text:
            return 0.0
        words = text.lower().split()
        if not words:
            return 0.0
        unique_words = len(set(words))
        total_words = len(words)
        if unique_words < 2:
            return 0.0
        entropy = math.log(max(unique_words, 2)) * total_words / 100.0
        self.stats["total_entropy"] += entropy
        return round(entropy, 4)

    def get_thermal_report(self) -> dict:
        total_routes = max(self.stats["thermal_routes"], 1)
        model_energy = defaultdict(float)
        model_count = defaultdict(int)
        for entry in self.query_energy_log:
            model_energy[entry["model"]] += entry["joules"]
            model_count[entry["model"]] += 1
        return {
            **self.stats, "carnot_efficiency": round(self.carnot_efficiency, 4),
            "avg_entropy": round(self.stats["total_entropy"] / total_routes, 4),
            "state_percentages": {k: round(v / total_routes, 4) for k, v in self.stats["state_distribution"].items()},
            "energy_by_model": {
                k: {"total_joules": round(v, 6), "queries": model_count[k],
                    "avg_joules": round(v / max(model_count[k], 1), 6)}
                for k, v in model_energy.items()
            },
        }
