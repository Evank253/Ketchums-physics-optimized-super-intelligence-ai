"""
Ketchum's Physics Optimized Super Intelligence
Physics Accuracy Engine — v2

Validates responses against physical constants and conservation laws.
"""

import math
import re
from typing import Optional


class PhysicsAccuracyEngine:

    CONSTANTS = {
        "speed_of_light": {"value": 299792458, "unit": "m/s", "symbol": "c"},
        "planck_constant": {"value": 6.62607015e-34, "unit": "J*s", "symbol": "h"},
        "boltzmann_constant": {"value": 1.380649e-23, "unit": "J/K", "symbol": "k_B"},
        "avogadro_number": {"value": 6.02214076e23, "unit": "mol^-1", "symbol": "N_A"},
        "electron_mass": {"value": 9.10938370e-31, "unit": "kg", "symbol": "m_e"},
        "proton_mass": {"value": 1.67262192e-27, "unit": "kg", "symbol": "m_p"},
        "gravitational_constant": {"value": 6.67430e-11, "unit": "m^3/(kg*s^2)", "symbol": "G"},
        "elementary_charge": {"value": 1.60217663e-19, "unit": "C", "symbol": "e"},
        "vacuum_permittivity": {"value": 8.85418781e-12, "unit": "F/m", "symbol": "e_0"},
        "vacuum_permeability": {"value": 1.25663706e-6, "unit": "H/m", "symbol": "mu_0"},
    }

    def __init__(self):
        self.validation_log = []
        self.stats = {"validations": 0, "violations_found": 0, "constants_checked": 0}

    def get_relevant_constants(self, prompt: str) -> dict:
        prompt_lower = prompt.lower()
        relevant = {}
        constant_keywords = {
            "speed_of_light": ["speed of light", "light speed", "c=", "photon", "relativity"],
            "planck_constant": ["planck", "quantum", "h=", "photon energy"],
            "boltzmann_constant": ["boltzmann", "temperature", "thermal", "entropy"],
            "avogadro_number": ["avogadro", "mole", "molar", "molecule"],
            "electron_mass": ["electron", "electron mass"],
            "proton_mass": ["proton", "proton mass", "nucleon"],
            "gravitational_constant": ["gravity", "gravitational", "G=", "newton"],
            "elementary_charge": ["charge", "electron charge", "coulomb"],
        }
        for const_name, keywords in constant_keywords.items():
            for keyword in keywords:
                if keyword in prompt_lower:
                    if const_name in self.CONSTANTS:
                        relevant[const_name] = self.CONSTANTS[const_name]
                    break
        self.stats["constants_checked"] += len(relevant)
        return relevant

    def validate_response(self, response: str, query_type: str) -> dict:
        self.stats["validations"] += 1
        flags = []
        warning = None

        if query_type not in {"math", "research", "analysis"}:
            return {"validated": True, "flags": [], "warning": None, "checked": False}

        speed_pattern = r"(\d+\.?\d*)\s*(?:x|·)?\s*10\^?(\d+)?\s*m/s"
        for match in re.finditer(speed_pattern, response):
            try:
                base = float(match.group(1))
                exponent = int(match.group(2)) if match.group(2) else 0
                value = base * (10 ** exponent)
                if value > 299792458 * 1.01:
                    flags.append({"type": "speed_exceeds_c", "value": value, "bound": 299792458})
            except (ValueError, TypeError):
                pass

        temp_pattern = r"-\s*(\d+\.?\d*)\s*K\b"
        for match in re.finditer(temp_pattern, response):
            try:
                value = float(match.group(1))
                if value > 0:
                    flags.append({"type": "negative_kelvin", "value": -value})
            except (ValueError, TypeError):
                pass

        if "infinite energy" in response.lower() and "not possible" not in response.lower():
            flags.append({"type": "infinite_energy_claim", "note": "Infinite energy claimed without caveat"})
        if "perpetual motion" in response.lower() and "impossible" not in response.lower():
            flags.append({"type": "perpetual_motion", "note": "Perpetual motion mentioned without impossibility note"})

        if flags:
            self.stats["violations_found"] += 1
            warning = f"Physics validation found {len(flags)} flag(s)"

        result = {"validated": len(flags) == 0, "flags": flags, "warning": warning, "checked": True}
        self.validation_log.append(result)
        return result

    def get_stats(self) -> dict:
        validation_rate = (self.stats["validations"] - self.stats["violations_found"]) / max(self.stats["validations"], 1)
        return {**self.stats, "validation_rate": round(validation_rate, 4), "constants_available": len(self.CONSTANTS)}
