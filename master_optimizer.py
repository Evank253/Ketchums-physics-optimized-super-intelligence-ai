"""
Ketchum's Physics Optimized Super Intelligence
Master Physics Optimizer — v2

Orchestrates all 15 physics engines.
Tracks real energy, uses compression-based metrics, trains reservoir readout.
"""

import time
from typing import Optional

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

from core.physics.quantum_field import QuantumFieldPreprocessor
from core.physics.tensor_compression import TensorNetworkCompressor
from core.physics.neuromorphic import NeuromorphicSpikeClassifier
from core.physics.statistical_mechanics import StatisticalMechanicsOptimizer
from core.physics.reversible_logic import ReversibleLogicEngine
from core.physics.photonic_executor import PhotonicParallelExecutor
from core.physics.reservoir_computing import ReservoirComputingAggregator
from core.physics.information_field import InformationFieldOptimizer
from core.physics.spintronic_memory import SpintronicMemory
from core.physics.wave_resonance import WaveResonanceEngine
from core.physics.relativistic_scheduler import RelativisticScheduler
from core.physics.thermodynamics import ThermodynamicEngine
from core.physics.quantum_compression import QuantumCompressionEngine
from core.physics.cold_computing import ColdComputingEngine
from core.physics.accuracy_engine import PhysicsAccuracyEngine


class MasterPhysicsOptimizer:

    def __init__(self, spintronic_db_path: str = ".spintronic.db"):
        self.quantum_field = QuantumFieldPreprocessor()
        self.tensor_compress = TensorNetworkCompressor()
        self.quantum_compress = QuantumCompressionEngine()
        self.thermodynamics = ThermodynamicEngine()
        self.reversible_logic = ReversibleLogicEngine()
        self.cold_computing = ColdComputingEngine()
        self.neuromorphic = NeuromorphicSpikeClassifier()
        self.reservoir = ReservoirComputingAggregator()
        self.stat_mechanics = StatisticalMechanicsOptimizer()
        self.photonic = PhotonicParallelExecutor()
        self.relativistic = RelativisticScheduler()
        self.info_field = InformationFieldOptimizer()
        self.wave_resonance = WaveResonanceEngine()
        self.spintronic = SpintronicMemory(db_path=spintronic_db_path)
        self.physics_accuracy = PhysicsAccuracyEngine()

    def _get_cpu_load(self) -> float:
        if HAS_PSUTIL:
            return psutil.cpu_percent(interval=0.1) / 100
        return 0.3

    async def pre_process(self, prompt: str) -> dict:
        start = time.time()
        cpu_load = self._get_cpu_load()

        superposition = self.quantum_field.create_superposition(prompt)
        collapsed = self.quantum_field.collapse_wave_function(superposition)
        quantum_prompt = self.quantum_field.optimize_prompt(prompt, collapsed)

        spike_result = self.neuromorphic.classify(prompt)
        query_type = spike_result["intent"]
        if collapsed["primary_prob"] > spike_result["confidence"]:
            query_type = collapsed["primary_intent"]

        thermal = self.thermodynamics.route_by_thermal_state(query_type, cpu_load)
        contracted = self.relativistic.length_contract_prompt(quantum_prompt, cpu_load)
        final_prompt = contracted["prompt"]

        models = ["gpt-4-turbo", "claude-3-opus", "claude-3-sonnet", "gemini-pro", "mistral-local"]
        model_selection = self.stat_mechanics.boltzmann_select(models, query_type)

        if thermal["thermal"]["state"] == "CRITICAL":
            model_selection["selected"] = "mistral-local"

        recycled = self.reversible_logic.get_recycled(f"prompt:{hash(prompt)}")
        spin_result = self.spintronic.read(prompt)
        cold_result = self.cold_computing.retrieve(str(hash(prompt)))

        physics_constants = self.physics_accuracy.get_relevant_constants(prompt)
        channel = self.info_field.get_channel_capacity(query_type)
        deadline = self.relativistic.assign_deadline(query_type)

        pre_ms = (time.time() - start) * 1000

        return {
            "optimized_prompt": final_prompt, "query_type": query_type,
            "quantum_prob": collapsed["primary_prob"], "spike_confidence": spike_result["confidence"],
            "uncertainty": collapsed["uncertainty"],
            "interference_shift": collapsed.get("interference_shift_bits", 0),
            "model_selected": model_selection["selected"],
            "boltzmann_prob": model_selection["probability"],
            "thermal_state": thermal["thermal"]["state"],
            "thermal_efficiency": thermal["efficiency"],
            "estimated_energy_j": thermal.get("estimated_energy_j", 0),
            "contracted": contracted["contracted"],
            "contraction_method": contracted.get("method", "unknown"),
            "cached_response": recycled or spin_result or cold_result,
            "physics_context": physics_constants, "channel_capacity": channel,
            "deadline_ms": deadline, "pre_process_ms": round(pre_ms, 2),
            "spike_data": spike_result["all_neurons"],
        }

    async def execute_parallel(self, prompt: str, models: list, executor) -> dict:
        return await self.photonic.parallel_execute(prompt, models, executor)

    async def post_process(self, prompt: str, responses: list, best: str,
                           query_type: str, model_used: str, start_time: float,
                           deadline_ms: float = 5000.0) -> dict:

        if len(responses) > 1:
            reservoir_result = self.reservoir.process_responses(responses, query_type)
            best = reservoir_result["best"]
            reservoir_method = reservoir_result.get("method", "unknown")
            reservoir_trained = reservoir_result.get("is_trained", False)
        else:
            reservoir_method = "single"
            reservoir_trained = False

        resonance = self.wave_resonance.calculate_resonance(prompt, best, query_type)
        tuned = self.wave_resonance.tune_response(best, resonance, query_type)

        entropy = self.info_field.calculate_shannon_entropy(tuned)
        snr = self.info_field.calculate_signal_to_noise(tuned)
        mi = self.info_field.calculate_mutual_information(prompt, tuned)
        kl_div = self.info_field.calculate_kl_divergence(prompt, tuned)
        dense = self.info_field.maximize_information_density(tuned)

        thermo_entropy = self.thermodynamics.calculate_entropy(dense)
        physics_check = self.physics_accuracy.validate_response(dense, query_type)
        text_compressed = self.quantum_compress.compress_text(dense)

        cache_value = {"response": dense, "query_type": query_type}
        cache_key = str(hash(prompt))
        self.cold_computing.store(cache_key, cache_value)
        self.spintronic.write(prompt, cache_value)
        self.reversible_logic.recycle_computation(f"prompt:{hash(prompt)}", cache_value)

        quality = entropy * 2 + snr["signal_to_noise"] * 0.5 + mi * 3 - kl_div * 0.1
        self.stat_mechanics.update_model_energy(model_used, quality, query_type)
        self.neuromorphic.stdp_learn(query_type, prompt, quality > 3.0)
        self.reservoir.add_training_example(dense, min(quality / 10.0, 1.0))

        latency = self.relativistic.measure_latency(start_time, deadline_ms=deadline_ms)
        energy = self.thermodynamics.track_query_energy(model_used, latency["actual_ms"], query_type)

        quality_final = quality + resonance["resonance_score"] * 2 + (1.0 if resonance["in_resonance"] else 0.0)

        return {
            "response": dense,
            "physics_metrics": {
                "resonance": resonance["resonance_score"],
                "in_resonance": resonance["in_resonance"],
                "coherence": resonance.get("mean_coherence", 0),
                "phase_consistency": resonance.get("phase_consistency", 0),
                "shannon_entropy": entropy, "thermo_entropy": thermo_entropy,
                "signal_to_noise": snr["signal_to_noise"],
                "mutual_info": mi, "kl_divergence": kl_div,
                "compression_ratio": text_compressed["ratio"],
                "latency_ms": latency["actual_ms"],
                "met_deadline": latency.get("met_deadline", True),
                "physics_validated": physics_check["validated"],
                "physics_flags": len(physics_check.get("flags", [])),
                "physics_warning": physics_check.get("warning"),
                "quality_score": round(quality_final, 4),
                "energy_joules": energy["total_joules"],
                "reservoir_method": reservoir_method,
                "reservoir_trained": reservoir_trained,
            },
        }

    def run_thermal_cycle(self) -> dict:
        return self.cold_computing.run_thermal_cycle()

    def get_full_report(self) -> dict:
        return {
            "quantum_field": self.quantum_field.get_field_stats(),
            "tensor_compression": self.tensor_compress.get_stats(),
            "neuromorphic": self.neuromorphic.get_stats(),
            "stat_mechanics": self.stat_mechanics.get_stats(),
            "reversible_logic": self.reversible_logic.get_stats(),
            "photonic": self.photonic.get_stats(),
            "reservoir": self.reservoir.get_stats(),
            "info_field": self.info_field.get_stats(),
            "spintronic": self.spintronic.get_stats(),
            "wave_resonance": self.wave_resonance.get_resonance_stats(),
            "relativistic": self.relativistic.get_scheduler_stats(),
            "thermodynamics": self.thermodynamics.get_thermal_report(),
            "quantum_compress": self.quantum_compress.get_compression_stats(),
            "cold_computing": self.cold_computing.get_stats(),
            "physics_accuracy": self.physics_accuracy.get_stats(),
        }
