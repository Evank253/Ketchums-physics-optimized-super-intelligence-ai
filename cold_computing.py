"""
Ketchum's Physics Optimized Super Intelligence
Cold Computing Engine — v2

PHYSICS:
- Cryogenic tiers: hot/warm/cold/frozen with decreasing energy cost
- Automatic thermal cycling: promote hot data, demote cold data
- Energy-aware tier transitions
"""

import math
import time
from typing import Optional
from collections import OrderedDict


class ColdComputingEngine:

    TIER_ENERGY = {
        "hot": {"store": 1.0, "retrieve": 0.1}, "warm": {"store": 0.5, "retrieve": 0.3},
        "cold": {"store": 0.2, "retrieve": 0.6}, "frozen": {"store": 0.1, "retrieve": 1.0},
    }
    PROMOTION_THRESHOLD = 3

    def __init__(self, max_hot: int = 100, max_warm: int = 500,
                 max_cold: int = 2000, max_frozen: int = 10000):
        self.tiers = {
            "hot": {"data": OrderedDict(), "max_size": max_hot},
            "warm": {"data": OrderedDict(), "max_size": max_warm},
            "cold": {"data": OrderedDict(), "max_size": max_cold},
            "frozen": {"data": OrderedDict(), "max_size": max_frozen},
        }
        self.access_tracking = {}
        self.energy_budget = 0.0
        self.stats = {
            "stores": 0, "retrieves": 0, "promotions": 0,
            "demotions": 0, "misses": 0, "thermal_cycles": 0, "total_energy": 0.0,
        }

    def store(self, key: str, value: any, tier: str = "warm") -> dict:
        self.stats["stores"] += 1
        if tier not in self.tiers:
            tier = "warm"
        while len(self.tiers[tier]["data"]) >= self.tiers[tier]["max_size"]:
            self._evict_from_tier(tier)

        self.tiers[tier]["data"][key] = {"value": value, "tier": tier, "stored_at": time.time()}
        self.access_tracking[key] = {"reads": 0, "last_access": time.time()}

        energy = self.TIER_ENERGY[tier]["store"]
        self.energy_budget += energy
        self.stats["total_energy"] += energy
        return {"stored": True, "tier": tier, "energy_cost": energy}

    def retrieve(self, key: str) -> Optional[any]:
        self.stats["retrieves"] += 1
        for tier_name in ["hot", "warm", "cold", "frozen"]:
            if key in self.tiers[tier_name]["data"]:
                if key in self.access_tracking:
                    self.access_tracking[key]["reads"] += 1
                    self.access_tracking[key]["last_access"] = time.time()
                energy = self.TIER_ENERGY[tier_name]["retrieve"]
                self.energy_budget += energy
                self.stats["total_energy"] += energy
                return self.tiers[tier_name]["data"][key]["value"]
        self.stats["misses"] += 1
        return None

    def promote(self, key: str):
        tier_order = ["frozen", "cold", "warm", "hot"]
        for i, tier_name in enumerate(tier_order):
            if key in self.tiers[tier_name]["data"]:
                if i < len(tier_order) - 1:
                    next_tier = tier_order[i + 1]
                    entry = self.tiers[tier_name]["data"].pop(key)
                    while len(self.tiers[next_tier]["data"]) >= self.tiers[next_tier]["max_size"]:
                        self._evict_from_tier(next_tier)
                    entry["tier"] = next_tier
                    self.tiers[next_tier]["data"][key] = entry
                    self.stats["promotions"] += 1
                    energy = self.TIER_ENERGY[tier_name]["retrieve"] + self.TIER_ENERGY[next_tier]["store"]
                    self.energy_budget += energy
                    self.stats["total_energy"] += energy
                break

    def demote(self, key: str):
        tier_order = ["hot", "warm", "cold", "frozen"]
        for i, tier_name in enumerate(tier_order):
            if key in self.tiers[tier_name]["data"]:
                if i < len(tier_order) - 1:
                    next_tier = tier_order[i + 1]
                    entry = self.tiers[tier_name]["data"].pop(key)
                    entry["tier"] = next_tier
                    self.tiers[next_tier]["data"][key] = entry
                    self.stats["demotions"] += 1
                    energy = self.TIER_ENERGY[next_tier]["store"]
                    self.energy_budget += energy
                    self.stats["total_energy"] += energy
                break

    def run_thermal_cycle(self) -> dict:
        self.stats["thermal_cycles"] += 1
        promotions = 0
        demotions = 0
        keys_to_promote = []
        keys_to_demote = []

        for key, tracking in self.access_tracking.items():
            if tracking["reads"] >= self.PROMOTION_THRESHOLD:
                keys_to_promote.append(key)
                tracking["reads"] = 0
            elif tracking["reads"] == 0 and time.time() - tracking["last_access"] > 3600:
                keys_to_demote.append(key)

        for key in keys_to_promote:
            self.promote(key)
            promotions += 1
        for key in keys_to_demote:
            self.demote(key)
            demotions += 1
            if key in self.access_tracking:
                self.access_tracking[key]["reads"] = 0

        return {
            "thermal_cycle": self.stats["thermal_cycles"],
            "promotions": promotions, "demotions": demotions,
            "tier_sizes": {name: len(tier["data"]) for name, tier in self.tiers.items()},
        }

    def _evict_from_tier(self, tier_name: str):
        if self.tiers[tier_name]["data"]:
            key, _ = self.tiers[tier_name]["data"].popitem(last=False)
            self.access_tracking.pop(key, None)

    def get_stats(self) -> dict:
        total_items = sum(len(tier["data"]) for tier in self.tiers.values())
        return {
            **self.stats, "total_items": total_items,
            "tier_utilization": {
                name: {"items": len(tier["data"]), "capacity": tier["max_size"],
                       "utilization": round(len(tier["data"]) / tier["max_size"], 4)}
                for name, tier in self.tiers.items()
            },
            "energy_budget": round(self.energy_budget, 4),
        }
