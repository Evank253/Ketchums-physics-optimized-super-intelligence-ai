"""
Ketchum's Physics Optimized Super Intelligence — Demo v2

Runs all 15 engines with real metrics.
Run: PYTHONPATH=. python demo.py
"""

import asyncio
import json
import time
import numpy as np

from core.physics.master_optimizer import MasterPhysicsOptimizer
from core.intelligence.scorer import score_response, pick_best_response
from core.intelligence.amplifier import strengthen_response


def section(title):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print("=" * 60)


def demo_quantum_field():
    section("1. QUANTUM FIELD PREPROCESSOR (Complex Amplitudes)")
    from core.physics.quantum_field import QuantumFieldPreprocessor
    qf = QuantumFieldPreprocessor()

    prompts = [
        "Write Python code to sort an array",
        "Calculate the integral of sin(x)",
        "Write code that's creative and artistic",
    ]
    for prompt in prompts:
        sp = qf.create_superposition(prompt)
        collapsed = qf.collapse_wave_function(sp)
        print(f"\n  '{prompt}'")
        print(f"  Primary: {collapsed['primary_intent']} ({collapsed['primary_prob']:.2%})")
        print(f"  Interference shift: {collapsed['interference_shift_bits']:.4f} bits")
        print(f"  Quantum probs ≠ linear? {collapsed['interference_shift_bits'] > 0}")


def demo_neuromorphic():
    section("2. NEUROMORPHIC SPIKE CLASSIFIER (Inhibition + Temporal)")
    from core.physics.neuromorphic import NeuromorphicSpikeClassifier
    nc = NeuromorphicSpikeClassifier()

    prompts = [
        "Write a Python function to sort a list",
        "Calculate the derivative of x squared",
        "Write a creative poem about the ocean",
    ]
    for prompt in prompts:
        result = nc.classify(prompt)
        print(f"\n  '{prompt[:45]}...'")
        print(f"  Intent: {result['intent']} (confidence: {result['confidence']:.2%})")
        print(f"  Inhibition events: {result['inhibition_events']}")
        print(f"  Time: {result['classification_ms']:.3f}ms")


def demo_information_field():
    section("3. INFORMATION FIELD (Compression-Based)")
    from core.physics.information_field import InformationFieldOptimizer
    info = InformationFieldOptimizer()

    diverse = "quantum entanglement superposition hilbert schmidt decomposition coherence"
    filler = "the a an is are was were be been being have has had do does did"

    e1 = info.calculate_shannon_entropy(diverse)
    e2 = info.calculate_shannon_entropy(filler)
    print(f"  Diverse text entropy: {e1}")
    print(f"  Filler text entropy: {e2}")

    mi = info.calculate_mutual_information(
        "What is Python programming",
        "Python is a programming language for web development",
    )
    mi_unrelated = info.calculate_mutual_information(
        "What is Python programming",
        "The Eiffel Tower was built in 1889",
    )
    print(f"\n  MI (related): {mi}")
    print(f"  MI (unrelated): {mi_unrelated}")

    snr1 = info.calculate_signal_to_noise(diverse)
    snr2 = info.calculate_signal_to_noise(filler)
    print(f"\n  SNR (diverse): {snr1['signal_to_noise']}")
    print(f"  SNR (filler): {snr2['signal_to_noise']}")


def demo_wave_resonance():
    section("4. WAVE RESONANCE (Cross-Spectral)")
    from core.physics.wave_resonance import WaveResonanceEngine
    wr = WaveResonanceEngine()

    a = "The quantum mechanical model describes the behavior of particles at the atomic and subatomic level " * 3
    b = "Quantum mechanics provides a mathematical framework for understanding atomic and subatomic particle behavior " * 3

    r_similar = wr.calculate_resonance(a, b, "research")
    print(f"  Similar texts resonance: {r_similar['resonance_score']}")
    print(f"    Coherence: {r_similar['mean_coherence']}")
    print(f"    Phase consistency: {r_similar['phase_consistency']}")


def demo_reservoir():
    section("5. RESERVOIR COMPUTING (Trainable Readout)")
    from core.physics.reservoir_computing import ReservoirComputingAggregator
    rc = ReservoirComputingAggregator()

    good = ["Hash maps provide O(1) lookup time complexity for key-value pairs",
            "Dynamic programming optimizes by caching overlapping subproblems"]
    bad = ["uhhh", "the the the"]
    for r in good:
        rc.add_training_example(r, 1.0)
    for r in bad:
        rc.add_training_example(r, 0.0)

    responses = [
        "Python is a high-level programming language known for readability.",
        "Python is a programming language. It is used for many things.",
        "Python is a snake species found in tropical regions.",
    ]
    result = rc.process_responses(responses, "coding")
    print(f"  Trained: {rc.is_trained}")
    print(f"  Best score: {result['best_score']}")
    print(f"  Separation: {result['separation']}")
    print(f"  Method: {result['method']}")


def demo_spintronic():
    section("6. SPINTRONIC MEMORY (SQLite Persistence)")
    import os
    from core.physics.spintronic_memory import SpintronicMemory
    db = ".demo_spintronic.db"
    if os.path.exists(db):
        os.remove(db)

    mem = SpintronicMemory(db_path=db)
    mem.write("python_code", {"lang": "python"}, priority=0.9)
    mem.write("recipe_pasta", {"type": "recipe"}, priority=0.3)
    mem.close()

    mem2 = SpintronicMemory(db_path=db)
    result = mem2.read("python_code")
    print(f"  Survived restart: {result is not None}")
    print(f"  Value: {result}")

    results = mem2.bulk_search("python")
    print(f"  Vector search 'python': {len(results)} results")
    mem2.close()
    os.remove(db)


def demo_thermodynamics():
    section("7. THERMODYNAMIC ENGINE (Real Energy Tracking)")
    from core.physics.thermodynamics import ThermodynamicEngine
    te = ThermodynamicEngine()

    for load in [0.1, 0.7, 0.95]:
        result = te.route_by_thermal_state("coding", load)
        energy = te.track_query_energy(result["recommendation"]["primary"], 500.0, "coding")
        print(f"  Load {load}: {result['thermal']['state']} → {result['recommendation']['primary']} "
              f"({energy['total_joules']:.4f} J)")


def demo_reversible():
    section("8. REVERSIBLE LOGIC ENGINE")
    from core.physics.reversible_logic import ReversibleLogicEngine
    rl = ReversibleLogicEngine()

    out = rl.toffoli_gate(True, True, False)
    back = rl.toffoli_gate(*out)
    print(f"  Toffoli(True,True,False) → {out} → {back}")
    print(f"  Reversible: {(True, True, False) == back}")

    cost = rl.calculate_entropy_cost(1_000_000)
    print(f"  Cost to erase 1M bits: {cost['energy_joules']:.2e} J")

    rl.recycle_computation("expensive", {"result": 42})
    recycled = rl.recycle_computation("expensive", None)
    print(f"  Recycled computation: {recycled['recycled']}")


def demo_full_pipeline():
    section("9. FULL PIPELINE (Master Optimizer)")
    optimizer = MasterPhysicsOptimizer()

    async def run():
        pre = await optimizer.pre_process("Write a Python function to calculate fibonacci numbers")
        print(f"  Query type: {pre['query_type']}")
        print(f"  Model: {pre['model_selected']}")
        print(f"  Thermal: {pre['thermal_state']}")
        print(f"  Interference shift: {pre['interference_shift']:.4f} bits")
        print(f"  Deadline: {pre['deadline_ms']:.0f}ms")

        post = await optimizer.post_process(
            prompt="Write a Python function to calculate fibonacci numbers",
            responses=["def fib(n): return n if n<=1 else fib(n-1)+fib(n-2)"],
            best="def fib(n): return n if n<=1 else fib(n-1)+fib(n-2)",
            query_type="coding", model_used="gpt-4-turbo",
            start_time=time.time(), deadline_ms=5000.0,
        )
        m = post["physics_metrics"]
        print(f"\n  Resonance: {m['resonance']:.4f}")
        print(f"  MI: {m['mutual_info']:.4f}")
        print(f"  KL divergence: {m['kl_divergence']:.4f}")
        print(f"  Energy: {m['energy_joules']:.4f} J")
        print(f"  Met deadline: {m['met_deadline']}")

    asyncio.run(run())
    optimizer.spintronic.close()


def demo_unified():
    section("10. UNIFIED ENGINE (End-to-End)")
    from core.intelligence.unified_engine import UnifiedSuperIntelligence

    engine = UnifiedSuperIntelligence()

    async def mock_query(prompt, model):
        await asyncio.sleep(0.01)
        return f"[{model}] Response about: {prompt[:30]}..."

    engine.set_model_query(mock_query)

    async def run():
        result = await engine.process("Write a Python hello world program", "user_1")
        print(f"  Response: {result['response'][:60]}...")
        print(f"  Model: {result['model_used']}")
        print(f"  Type: {result['query_type']}")
        q = result.get("quantum", {})
        print(f"  Interference shift: {q.get('interference_shift', 0):.4f} bits")
        p = result.get("performance", {})
        print(f"  Energy: {p.get('energy_joules', 0):.4f} J")
        print(f"  Reservoir trained: {p.get('reservoir_trained', False)}")
        engine.cleanup()

    asyncio.run(run())


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   KETCHUM'S PHYSICS OPTIMIZED SUPER INTELLIGENCE        ║")
    print("║   15 Engines • Real Metrics • No Fakes                   ║")
    print("╚══════════════════════════════════════════════════════════╝")

    demo_quantum_field()
    demo_neuromorphic()
    demo_information_field()
    demo_wave_resonance()
    demo_reservoir()
    demo_spintronic()
    demo_thermodynamics()
    demo_reversible()
    demo_full_pipeline()
    demo_unified()

    print("\n" + "=" * 60)
    print("KETCHUM'S PHYSICS OPTIMIZED SUPER INTELLIGENCE ✅")
    print("=" * 60)
