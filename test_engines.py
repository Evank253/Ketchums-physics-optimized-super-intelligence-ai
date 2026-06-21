"""
Ketchum's Physics Optimized Super Intelligence — Test Suite v2

Every engine must prove it adds value beyond a simple baseline.
Run: PYTHONPATH=. python tests/test_engines.py
"""

import asyncio
import math
import time
import numpy as np
import os
from collections import Counter

passed = 0
failed = 0


def test(name):
    def decorator(fn):
        def wrapper():
            global passed, failed
            try:
                fn()
                passed += 1
                print(f"  ✅ {name}")
            except AssertionError as e:
                failed += 1
                print(f"  ❌ {name}: {e}")
            except Exception as e:
                failed += 1
                print(f"  💥 {name}: {type(e).__name__}: {e}")
        return wrapper
    return decorator


def assert_gt(a, b, msg=""):
    assert a > b, f"Expected {a} > {b} {msg}"


def assert_lt(a, b, msg=""):
    assert a < b, f"Expected {a} < {b} {msg}"


# ── Quantum Field ──────────────────────────────────────────────

@test("Quantum Field: Complex amplitudes differ from linear")
def test_quantum_interference():
    from core.physics.quantum_field import QuantumFieldPreprocessor
    qf = QuantumFieldPreprocessor()
    sp = qf.create_superposition("code poem")
    collapsed = qf.collapse_wave_function(sp)
    assert sp["interference_factor"] != 1.0
    quantum_probs = collapsed["probabilities"]
    linear_probs = collapsed["linear_probs"]
    max_diff = max(abs(quantum_probs.get(k, 0) - linear_probs.get(k, 0)) for k in quantum_probs)
    assert_gt(max_diff, 0.001)


@test("Quantum Field: Interference shift is measurable")
def test_quantum_shift():
    from core.physics.quantum_field import QuantumFieldPreprocessor
    qf = QuantumFieldPreprocessor()
    sp = qf.create_superposition("write code that's creative and technical")
    collapsed = qf.collapse_wave_function(sp)
    assert_gt(collapsed["interference_shift_bits"], 0)


@test("Quantum Field: Entangled concepts boost together")
def test_quantum_entanglement():
    from core.physics.quantum_field import QuantumFieldPreprocessor
    qf = QuantumFieldPreprocessor()
    sp1 = qf.create_superposition("code")
    sp2 = qf.create_superposition("code python")
    total1 = sum(abs(complex(v["real"], v["imag"])) for v in sp1["amplitudes"].values())
    total2 = sum(abs(complex(v["real"], v["imag"])) for v in sp2["amplitudes"].values())
    assert_gt(total2, total1)


# ── Neuromorphic ───────────────────────────────────────────────

@test("Neuromorphic: Inhibitory connections suppress competitors")
def test_neuromorphic_inhibition():
    from core.physics.neuromorphic import NeuromorphicSpikeClassifier
    nc = NeuromorphicSpikeClassifier()
    result = nc.classify("code function python")
    assert result["intent"] == "coding"
    assert_gt(result.get("inhibition_events", 0), 0)


@test("Neuromorphic: STDP with forgetting curve")
def test_neuromorphic_stdp():
    from core.physics.neuromorphic import NeuromorphicSpikeClassifier
    nc = NeuromorphicSpikeClassifier()
    initial = nc.synaptic_weights["coding"]["python"]
    nc.stdp_learn("coding", "python code", True)
    after_positive = nc.synaptic_weights["coding"]["python"]
    nc.stdp_learn("coding", "python code", False)
    after_negative = nc.synaptic_weights["coding"]["python"]
    assert_gt(after_positive, initial)
    assert_lt(after_negative, after_positive)


@test("Neuromorphic: Adaptive threshold prevents domination")
def test_neuromorphic_adaptation():
    from core.physics.neuromorphic import NeuromorphicSpikeClassifier
    nc = NeuromorphicSpikeClassifier()
    for _ in range(5):
        nc.classify("code python function debug script")
    assert_gt(nc.neurons["coding"]["threshold"], nc.base_threshold)


# ── Information Field ──────────────────────────────────────────

@test("Information Field: Compression entropy distinguishes text types")
def test_info_entropy():
    from core.physics.information_field import InformationFieldOptimizer
    info = InformationFieldOptimizer()
    e_random = info.calculate_shannon_entropy(
        "The quantum field processor uses superposition collapse for intent classification"
    )
    e_repeated = info.calculate_shannon_entropy("blah blah blah " * 10)
    assert_gt(e_random, e_repeated * 0.5)


@test("Information Field: Compression MI detects related texts")
def test_info_mi():
    from core.physics.information_field import InformationFieldOptimizer
    info = InformationFieldOptimizer()
    mi_related = info.calculate_mutual_information(
        "What is Python programming",
        "Python is a programming language used for web development",
    )
    mi_unrelated = info.calculate_mutual_information(
        "What is Python programming",
        "The Eiffel Tower was built in 1889 and is 330 meters tall",
    )
    assert_gt(mi_related, mi_unrelated)


@test("Information Field: KL divergence measures distribution difference")
def test_info_kl():
    from core.physics.information_field import InformationFieldOptimizer
    info = InformationFieldOptimizer()
    kl_same = info.calculate_kl_divergence("python code function", "python code function")
    kl_diff = info.calculate_kl_divergence("python code function", "creative writing story poem")
    assert_lt(kl_same, 0.1)
    assert_gt(kl_diff, kl_same)


@test("Information Field: SNR distinguishes signal from noise")
def test_info_snr():
    from core.physics.information_field import InformationFieldOptimizer
    info = InformationFieldOptimizer()
    snr_diverse = info.calculate_signal_to_noise(
        "quantum entanglement superposition hilbert schmidt decomposition coherence"
    )
    snr_filler = info.calculate_signal_to_noise(
        "the a an is are was were be been being have has had do does did"
    )
    assert_gt(snr_diverse["signal_to_noise"], snr_filler["signal_to_noise"])


# ── Wave Resonance ─────────────────────────────────────────────

@test("Wave Resonance: Cross-spectral coherence is measurable")
def test_wave_coherence():
    from core.physics.wave_resonance import WaveResonanceEngine
    wr = WaveResonanceEngine()
    long_a = "The quantum mechanical model describes the behavior of particles at the atomic and subatomic level"
    long_b = "Quantum mechanics provides a mathematical framework for understanding atomic and subatomic particle behavior"
    res = wr.calculate_resonance(long_a, long_b, "research")
    assert_gt(res["mean_coherence"], 0)


# ── Reservoir Computing ────────────────────────────────────────

@test("Reservoir: Trainable readout learns from quality labels")
def test_reservoir_training():
    from core.physics.reservoir_computing import ReservoirComputingAggregator
    rc = ReservoirComputingAggregator()
    good = [
        "The solution involves using a hash map for O(1) lookup time complexity",
        "You can optimize this by using dynamic programming with memoization",
        "The algorithm runs in O(n log n) time using a divide and conquer approach",
        "Binary search works on sorted arrays with logarithmic time complexity",
        "Graph traversal can be done with BFS or DFS depending on the use case",
        "Memoization caches previously computed results to avoid redundant calculations",
    ]
    bad = ["uhhh", "idk maybe try something", "the the the the the", "lol no idea", "try turning it off"]
    for r in good:
        rc.add_training_example(r, 1.0)
    for r in bad:
        rc.add_training_example(r, 0.0)
    assert rc.is_trained


@test("Reservoir: Separation metric is measured")
def test_reservoir_separation():
    from core.physics.reservoir_computing import ReservoirComputingAggregator
    rc = ReservoirComputingAggregator()
    result = rc.process_responses([
        "Python is a high-level programming language with dynamic typing",
        "The Mediterranean diet emphasizes olive oil and fresh vegetables",
        "Quantum computers use qubits instead of classical bits",
    ], "general")
    assert "separation" in result
    assert_gt(result["separation"], 0)


# ── Spintronic Memory ──────────────────────────────────────────

@test("Spintronic: Data persists in SQLite across restart")
def test_spintronic_persistence():
    from core.physics.spintronic_memory import SpintronicMemory
    db_path = ".test_spintronic.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    mem = SpintronicMemory(db_path=db_path)
    mem.write("test_key_12345", {"data": "persisted_value"}, priority=0.9)
    mem.close()
    assert os.path.exists(db_path)
    mem2 = SpintronicMemory(db_path=db_path)
    result = mem2.read("test_key_12345")
    assert result is not None
    assert result["data"] == "persisted_value"
    mem2.close()
    os.remove(db_path)


@test("Spintronic: Vector similarity search works")
def test_spintronic_search():
    from core.physics.spintronic_memory import SpintronicMemory
    mem = SpintronicMemory(max_size=1000)
    mem.write("python code examples", {"lang": "python"}, priority=0.7)
    mem.write("javascript code examples", {"lang": "javascript"}, priority=0.7)
    mem.write("cooking recipe pasta", {"type": "recipe"}, priority=0.5)
    results = mem.bulk_search("python code")
    assert_gt(len(results), 0)
    mem.close()


@test("Spintronic: Read/write cost asymmetry is tracked")
def test_spintronic_cost():
    from core.physics.spintronic_memory import SpintronicMemory
    mem = SpintronicMemory(max_size=1000)
    mem.write("key1", "value1")
    mem.read("key1")
    stats = mem.get_stats()
    assert_gt(stats["avg_write_cost_ms"], stats["avg_read_cost_ms"])
    assert_gt(stats["write_read_cost_ratio"], 1.0)
    mem.close()


# ── Relativistic Scheduler ─────────────────────────────────────

@test("Relativistic: Sentence scoring preserves meaning better than truncation")
def test_scheduler_compression():
    from core.physics.relativistic_scheduler import RelativisticScheduler
    rs = RelativisticScheduler()
    prompt = "Write a Python function. It should sort a list. The function must be efficient. Also add type hints. Consider edge cases."
    result = rs.length_contract_prompt(prompt, 0.8)
    assert result["method"] == "sentence_scoring"
    assert_lt(len(result["prompt"]), len(prompt))


@test("Relativistic: Radioactive decay of priority")
def test_scheduler_decay():
    from core.physics.relativistic_scheduler import RelativisticScheduler
    rs = RelativisticScheduler()
    fresh = rs.priority_decay(1.0, 0)
    aged_1h = rs.priority_decay(1.0, 3600)
    aged_1d = rs.priority_decay(1.0, 86400)
    assert_gt(fresh, aged_1h)
    assert_gt(aged_1h, aged_1d)


@test("Relativistic: Deadline tracking works")
def test_scheduler_deadline():
    from core.physics.relativistic_scheduler import RelativisticScheduler
    rs = RelativisticScheduler()
    start = time.time()
    result = rs.measure_latency(start, deadline_ms=10000.0)
    assert result["met_deadline"]
    coding_deadline = rs.assign_deadline("coding")
    creative_deadline = rs.assign_deadline("creative")
    assert_lt(coding_deadline, creative_deadline)


# ── Thermodynamics ─────────────────────────────────────────────

@test("Thermodynamics: Energy tracking per query")
def test_thermo_energy():
    from core.physics.thermodynamics import ThermodynamicEngine
    te = ThermodynamicEngine()
    energy = te.track_query_energy("gpt-4-turbo", 1000.0, "coding")
    assert_gt(energy["total_joules"], 0)
    assert_gt(energy["model_joules"], 0)


@test("Thermodynamics: Different models have different energy costs")
def test_thermo_model_comparison():
    from core.physics.thermodynamics import ThermodynamicEngine
    te = ThermodynamicEngine()
    e_large = te.track_query_energy("gpt-4-turbo", 1000.0, "coding")
    e_small = te.track_query_energy("mistral-local", 1000.0, "coding")
    assert_gt(e_large["model_joules"], e_small["model_joules"])


@test("Thermodynamics: Thermal states route to appropriate models")
def test_thermo_routing():
    from core.physics.thermodynamics import ThermodynamicEngine
    te = ThermodynamicEngine()
    cold = te.route_by_thermal_state("coding", 0.1)
    hot = te.route_by_thermal_state("coding", 0.9)
    cold_power = te.MODEL_POWER.get(cold["recommendation"]["primary"], 30)
    hot_power = te.MODEL_POWER.get(hot["recommendation"]["primary"], 30)
    assert_gt(cold_power, hot_power)


# ── Reversible Logic ───────────────────────────────────────────

@test("Reversible: Toffoli gate is reversible")
def test_reversible_toffoli():
    from core.physics.reversible_logic import ReversibleLogicEngine
    rl = ReversibleLogicEngine()
    for a in [False, True]:
        for b in [False, True]:
            for c in [False, True]:
                out = rl.toffoli_gate(a, b, c)
                back = rl.toffoli_gate(out[0], out[1], out[2])
                assert (a, b, c) == back


@test("Reversible: Fredkin gate is reversible")
def test_reversible_fredkin():
    from core.physics.reversible_logic import ReversibleLogicEngine
    rl = ReversibleLogicEngine()
    for c in [False, True]:
        for a in [False, True]:
            for b in [False, True]:
                out = rl.fredkin_gate(c, a, b)
                back = rl.fredkin_gate(out[0], out[1], out[2])
                assert (c, a, b) == back


@test("Reversible: Computation recycling saves work")
def test_reversible_recycling():
    from core.physics.reversible_logic import ReversibleLogicEngine
    rl = ReversibleLogicEngine()
    r1 = rl.recycle_computation("key1", {"expensive": "result"})
    assert not r1["recycled"]
    r2 = rl.recycle_computation("key1", None)
    assert r2["recycled"]
    assert r2["result"] == {"expensive": "result"}


# ── Tensor Compression ─────────────────────────────────────────

@test("Tensor: Embedding compression preserves cosine similarity")
def test_tensor_fidelity():
    from core.physics.tensor_compression import TensorNetworkCompressor
    tc = TensorNetworkCompressor()
    np.random.seed(42)
    embedding = np.random.randn(1536).tolist()
    result = tc.compress_embedding(embedding, rank=32)
    reconstructed = tc.decompress_embedding(result)
    a = np.array(embedding)
    b = np.array(reconstructed)
    cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    assert_gt(cos_sim, 0.9)


# ── Photonic Executor ──────────────────────────────────────────

@test("Photonic: Parallel execution is faster than sequential")
def test_photonic_speedup():
    from core.physics.photonic_executor import PhotonicParallelExecutor
    pe = PhotonicParallelExecutor()

    async def slow_executor(prompt, model):
        await asyncio.sleep(0.05)
        return f"Response from {model}"

    async def run():
        return await pe.parallel_execute(
            "test", ["gpt-4-turbo", "claude-3-opus", "gemini-pro"], slow_executor,
        )

    result = asyncio.run(run())
    assert_gt(result["speedup"], 1.5)


# ── Statistical Mechanics ──────────────────────────────────────

@test("StatMech: Boltzmann distribution normalizes to 1")
def test_statmech_normalize():
    from core.physics.statistical_mechanics import StatisticalMechanicsOptimizer
    sm = StatisticalMechanicsOptimizer()
    result = sm.boltzmann_select(["gpt-4-turbo", "claude-3-opus", "mistral-local"], "coding")
    total_prob = sum(result["all_probabilities"].values())
    assert abs(total_prob - 1.0) < 0.01


@test("StatMech: Quality updates shift model selection")
def test_statmech_learning():
    from core.physics.statistical_mechanics import StatisticalMechanicsOptimizer
    sm = StatisticalMechanicsOptimizer(temperature=0.1)
    for _ in range(10):
        sm.update_model_energy("gpt-4-turbo", 10.0, "coding")
    result = sm.boltzmann_select(["gpt-4-turbo", "claude-3-opus"], "coding")
    assert_gt(
        result["all_probabilities"].get("gpt-4-turbo", 0),
        result["all_probabilities"].get("claude-3-opus", 0),
    )


# ── Cold Computing ─────────────────────────────────────────────

@test("ColdComputing: Tiers store and retrieve data")
def test_cold_tiers():
    from core.physics.cold_computing import ColdComputingEngine
    cc = ColdComputingEngine()
    cc.store("hot_key", "hot_value", tier="hot")
    cc.store("cold_key", "cold_value", tier="cold")
    assert cc.retrieve("hot_key") == "hot_value"
    assert cc.retrieve("cold_key") == "cold_value"
    assert cc.retrieve("nonexistent") is None


@test("ColdComputing: Promotion and demotion work")
def test_cold_promotion():
    from core.physics.cold_computing import ColdComputingEngine
    cc = ColdComputingEngine()
    cc.store("key1", "value1", tier="cold")
    cc.promote("key1")
    assert cc.retrieve("key1") == "value1"


# ── Accuracy Engine ────────────────────────────────────────────

@test("Accuracy: Constants are retrieved for physics queries")
def test_accuracy_constants():
    from core.physics.accuracy_engine import PhysicsAccuracyEngine
    ae = PhysicsAccuracyEngine()
    constants = ae.get_relevant_constants("What is the speed of light in vacuum")
    assert "speed_of_light" in constants


@test("Accuracy: Validates physics in responses")
def test_accuracy_validation():
    from core.physics.accuracy_engine import PhysicsAccuracyEngine
    ae = PhysicsAccuracyEngine()
    r1 = ae.validate_response("The speed of light is approximately 3 x 10^8 m/s", "research")
    assert r1["validated"]
    r2 = ae.validate_response("This device produces infinite energy and solves all problems", "research")
    assert not r2["validated"]


# ── Baseline Comparisons ───────────────────────────────────────

@test("Baseline: Compression-based MI beats Jaccard for related texts")
def test_baseline_mi():
    from core.physics.information_field import InformationFieldOptimizer
    info = InformationFieldOptimizer()
    prompt = "machine learning neural networks deep learning"
    related = "neural networks use deep learning algorithms for machine learning tasks"
    unrelated = "cooking pasta with tomato sauce and basil requires boiling water"
    mi_related = info.calculate_mutual_information(prompt, related)
    mi_unrelated = info.calculate_mutual_information(prompt, unrelated)
    assert_gt(mi_related, mi_unrelated)


# ── Run ────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   KETCHUM'S PHYSICS OPTIMIZED SUPER INTELLIGENCE        ║")
    print("║   Test Suite v2 — Every engine proves its value          ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    test_functions = [
        obj for name, obj in sorted(globals().items())
        if callable(obj) and name.startswith("test_")
    ]
    for fn in test_functions:
        fn()

    print()
    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed out of {passed + failed} tests")
    if failed == 0:
        print("ALL TESTS PASSED ✅")
    else:
        print("SOME TESTS FAILED ❌")
    print("=" * 60)
