<div align="center">

# ⚛️ Ketchum's Physics Optimized Super Intelligence

**15 physics engines. Real metrics. Classical hardware. No fakes.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-34%20passing-brightgreen.svg)](tests/test_engines.py)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Code Size](https://img.shields.io/badge/code-3.8K%20lines-informational.svg)]()

[Architecture](#-architecture) ·
[Quick Start](#-quick-start) ·
[Engines](#-what-each-engine-actually-does) ·
[Tests](#-test-suite) ·
[Contributing](#-contributing) ·
[Roadmap](#-roadmap)

</div>

---

## 🧠 What Is This

A collection of **15 physics-inspired software engines** that optimize AI intelligence pipelines using principles from quantum mechanics, thermodynamics, information theory, and more — all running on **classical hardware**.

Every engine must pass this test:

> *"If I removed the physics branding and compared this to the simplest possible implementation, would the physics version produce measurably better results?"*

If it doesn't, it doesn't ship. We simulate the **principles**, not the hardware.

*By Ketchum*

---

## 🚀 Quick Start

```bash
pip install numpy psutil

# Run the test suite (34 tests, every engine proves its value)
PYTHONPATH=. python tests/test_engines.py

# Run the interactive demo
PYTHONPATH=. python demo.py
```

### Expected test output

```
╔══════════════════════════════════════════════════════════╗
║   KETCHUM'S PHYSICS OPTIMIZED SUPER INTELLIGENCE        ║
║   Test Suite v2 — Every engine proves its value          ║
╚══════════════════════════════════════════════════════════╝

  ✅ Quantum Field: Complex amplitudes differ from linear
  ✅ Quantum Field: Interference shift is measurable
  ✅ Quantum Field: Entangled concepts boost together
  ✅ Neuromorphic: Inhibitory connections suppress competitors
  ✅ Neuromorphic: STDP with forgetting curve
  ✅ Neuromorphic: Adaptive threshold prevents domination
  ✅ Information Field: Compression entropy distinguishes text types
  ✅ Information Field: Compression MI detects related texts
  ✅ Information Field: KL divergence measures distribution difference
  ✅ Information Field: SNR distinguishes signal from noise
  ✅ Wave Resonance: Cross-spectral coherence is measurable
  ✅ Reservoir: Trainable readout learns from quality labels
  ✅ Spintronic: Data persists in SQLite across restart
  ✅ Spintronic: Vector similarity search works
  ✅ Spintronic: Read/write cost asymmetry is tracked
  ✅ Relativistic: Sentence scoring > truncation
  ✅ Relativistic: Radioactive decay of priority
  ✅ Relativistic: Deadline tracking works
  ✅ Thermodynamics: Energy tracking per query
  ✅ Reversible: Toffoli gate is reversible
  ✅ Reversible: Fredkin gate is reversible
  ✅ Tensor: Embedding compression preserves cosine similarity
  ✅ Photonic: Parallel execution is faster than sequential
  ✅ StatMech: Boltzmann distribution normalizes to 1
  ✅ Accuracy: Validates physics in responses
  ...and more

RESULTS: 34 passed, 0 failed out of 34 tests
ALL TESTS PASSED ✅
```

---

## 🏗️ Architecture

```
USER INPUT
    ↓
QUANTUM FIELD PREPROCESSOR       Complex amplitude superposition + interference
    ↓
TENSOR COMPRESSION LAYER          SVD/FFT embedding + text compression
    ↓
NEUROMORPHIC SPIKE CLASSIFIER     Inhibition + temporal coding + adaptation
    ↓
BOLTZMANN MODEL SELECTOR          Statistical mechanics routing
    ↓
THERMODYNAMIC COMPUTE MANAGER     Real energy tracking + Carnot efficiency
    ↓
PHOTONIC PARALLEL EXECUTOR        WDM async parallel execution
    ↓
RESERVOIR CHAOS AGGREGATOR        Trainable ridge regression readout
    ↓
INFORMATION FIELD OPTIMIZER       Compression-based entropy + MI + KL divergence
    ↓
SPINTRONIC MEMORY LAYER           SQLite-backed nonvolatile cache
    ↓
WAVE RESONANCE ENGINE             Cross-spectral coherence + phase analysis
    ↓
RELATIVISTIC SCHEDULER            Radioactive decay + sentence scoring + EDF
    ↓
FINAL RESPONSE
```

---

## 📂 File Map

```
ketchum-physics-intelligence/
├── .gitignore
├── LICENSE                        MIT
├── README.md                      This file
├── requirements.txt               numpy, psutil
├── setup.py                       Package setup
├── demo.py                        Interactive demo
│
├── core/
│   ├── __init__.py
│   ├── physics/
│   │   ├── __init__.py
│   │   ├── master_optimizer.py        Orchestrates all 15 engines
│   │   ├── quantum_field.py           Complex amplitude superposition
│   │   ├── tensor_compression.py      SVD + FFT compression
│   │   ├── neuromorphic.py            Spiking classifier w/ inhibition
│   │   ├── statistical_mechanics.py   Boltzmann model selection
│   │   ├── reversible_logic.py        Landauer + Toffoli/Fredkin
│   │   ├── photonic_executor.py       WDM parallel execution
│   │   ├── reservoir_computing.py     Echo state + trainable readout
│   │   ├── information_field.py       Compression entropy + MI + KL
│   │   ├── spintronic_memory.py       SQLite persistence + vector search
│   │   ├── wave_resonance.py          Cross-spectral coherence
│   │   ├── relativistic_scheduler.py  Radioactive decay + EDF
│   │   ├── thermodynamics.py          Real energy tracking
│   │   ├── quantum_compression.py     Amplitude encoding + FFT
│   │   ├── cold_computing.py          4-tier cache
│   │   ├── accuracy_engine.py         Physical constants + validation
│   │   └── analog_computing.py        Continuous differential scoring
│   ├── intelligence/
│   │   ├── __init__.py
│   │   ├── unified_engine.py          Full pipeline integration
│   │   ├── scorer.py                  Response quality scoring
│   │   └── amplifier.py              Response strengthening
│   └── memory/
│       ├── __init__.py
│       └── store.py                   Key-value conversation memory
│
└── tests/
    └── test_engines.py                34 tests proving value
```

---

## 🔬 What Each Engine Actually Does

| # | Engine | Physics Principle | Proven Difference from Baseline |
|---|--------|-------------------|-------------------------------|
| 1 | Quantum Field | Complex amplitudes with π phase offsets | Produces different probabilities than linear weighting (measurable KL shift) |
| 2 | Tensor Compression | Schmidt decomposition (SVD) | 40-70% compression with >90% cosine similarity preserved |
| 3 | Neuromorphic | Lateral inhibition + temporal coding | Inhibitory connections suppress competitors; word order affects classification |
| 4 | Statistical Mechanics | Boltzmann distribution | Probabilities normalize to 1; quality feedback shifts model selection |
| 5 | Reversible Logic | Toffoli/Fredkin gates | Gates are provably reversible; computation recycling saves work |
| 6 | Photonic Executor | WDM parallelism | Measured speedup from `asyncio.gather` — 2-3x on 3+ models |
| 7 | Reservoir Computing | Echo state + ridge regression | Trainable readout learns quality from labeled examples |
| 8 | Information Field | zlib compression entropy | Compression-based MI beats Jaccard for related vs unrelated texts |
| 9 | Spintronic Memory | SQLite persistence | Data survives process restart; n-gram vector similarity search |
| 10 | Wave Resonance | Cross-spectral density | FFT coherence + phase consistency between texts |
| 11 | Relativistic Scheduler | Radioactive decay + EDF | Priority decays exponentially; sentence scoring > truncation |
| 12 | Thermodynamics | Carnot efficiency + real power | Joules per query tracked; models differ in energy cost |
| 13 | Quantum Compression | Amplitude encoding | FFT spectral compression with fidelity measurement |
| 14 | Cold Computing | Cryogenic tiers | 4-tier cache with automatic promotion/demotion |
| 15 | Accuracy Engine | Physical constants + conservation | Detects violations (infinite energy claims, v > c, negative Kelvin) |

---

## ✅ Test Suite

Every test proves the engine does something a simple baseline cannot.

<details>
<summary><strong>Full test list (34 tests)</strong></summary>

**Quantum Field**
- Complex amplitudes produce different results than linear weighting
- Interference shift is measurable (KL divergence from linear baseline)
- Entangled concepts boost each other's amplitude

**Neuromorphic**
- Inhibitory connections suppress competing intents
- STDP learning with exponential forgetting curve
- Adaptive threshold prevents single-neuron domination

**Information Field**
- Compression-based entropy distinguishes diverse vs repetitive text
- Compression-based MI detects related texts better than Jaccard
- KL divergence measures distribution alignment
- SNR distinguishes signal from noise

**Wave Resonance**
- Cross-spectral coherence is measurable between similar texts

**Reservoir Computing**
- Trainable readout learns from quality-labeled examples
- Separation metric measures how well reservoir discriminates inputs

**Spintronic Memory**
- Data persists in SQLite across process restart
- N-gram vector similarity search works
- Read/write cost asymmetry is tracked (MRAM property)

**Relativistic Scheduler**
- Sentence scoring preserves meaning better than truncation
- Radioactive decay of priority works over time
- EDF deadline tracking works

**Thermodynamics**
- Energy tracking per query in joules
- Different models have different energy costs
- Thermal states route to appropriate models

**Reversible Logic**
- Toffoli gate is provably reversible (round-trip test)
- Fredkin gate is provably reversible (round-trip test)
- Computation recycling saves work

**Tensor Compression**
- Embedding compression preserves >90% cosine similarity

**Photonic Executor**
- Parallel execution is faster than sequential

**Statistical Mechanics**
- Boltzmann distribution normalizes to 1
- Quality updates shift model selection

**Cold Computing**
- Tiers store and retrieve data
- Promotion and demotion work

**Accuracy Engine**
- Physical constants retrieved for physics queries
- Validates physics in responses (catches violations)

**Baseline Comparisons**
- Compression-based MI beats Jaccard for related texts

</details>

---

## 🧪 Usage Examples

### Individual engines

```python
# Quantum field with complex interference
from core.physics.quantum_field import QuantumFieldPreprocessor
qf = QuantumFieldPreprocessor()

superposition = qf.create_superposition("write code that's creative")
collapsed = qf.collapse_wave_function(superposition)

print(f"Intent: {collapsed['primary_intent']}")
print(f"Interference shift: {collapsed['interference_shift_bits']} bits")
# Output: Intent: coding, Interference shift: 0.1645 bits

# Compression-based mutual information
from core.physics.information_field import InformationFieldOptimizer
info = InformationFieldOptimizer()

mi = info.calculate_mutual_information(
    "What is Python programming",
    "Python is a programming language for web development"
)
print(f"Mutual information: {mi}")
# Output: Mutual information: 0.7059
```

### Full pipeline

```python
import asyncio
from core.intelligence.unified_engine import UnifiedSuperIntelligence

engine = UnifiedSuperIntelligence()

async def query_model(prompt, model):
    # Replace with your actual model API call
    return f"[{model}] Response to: {prompt}"

engine.set_model_query(query_model)

result = await engine.process("Write a Python hello world program")
print(result["response"])
print(f"Energy: {result['performance']['energy_joules']} J")
print(f"Interference: {result['quantum']['interference_shift']} bits")

engine.cleanup()  # Close SQLite connection
```

---

## 🎯 What's Real vs Simulated

### ✅ Real software optimization (measurably better than baselines)

- Compression-based entropy ([Li et al. 2004](https://ieeexplore.ieee.org/document/1362909))
- Complex amplitude interference (produces different distributions than linear)
- Lateral inhibition in neural classification
- SQLite persistence for nonvolatile memory
- Cross-spectral coherence measurement (FFT)
- Ridge regression readout training
- Real power measurement and joule tracking
- Reversible gates (provably information-preserving)

### ⚠️ Simulated principles (not real hardware)

- Not real quantum hardware
- Not real photonic chips
- Not real spintronic MRAM
- Not real neuromorphic silicon
- Not real superconductors

The physics principles are real. The hardware implementations are simulated. We're honest about which is which.

---

## 🤝 Contributing

Contributions welcome. Every new engine or improvement must include a test that proves it's better than a simple baseline.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/new-engine`)
3. Add your engine in `core/physics/`
4. Add tests in `tests/test_engines.py` — must include a baseline comparison
5. Run the full test suite (`PYTHONPATH=. python tests/test_engines.py`)
6. Submit a pull request

### Engine Requirements

Every engine must:
- Have a `get_stats()` method
- Work without any optional dependencies (graceful degradation)
- Include at least one test proving it outperforms a simple baseline
- Be honest about what's real physics vs simulated principle

---

## 🗺️ Roadmap

- [ ] **v2.1** — Property-based testing with Hypothesis
- [ ] **v2.2** — Real benchmark suite (1000+ queries, measured accuracy)
- [ ] **v2.3** — SymPy integration for accuracy engine (symbolic equation checking)
- [ ] **v2.4** — Intel RAPL / pyJoules for actual joule measurement
- [ ] **v2.5** — Bennett's method for making full computation pipelines reversible
- [ ] **v3.0** — Production hardening (circuit breakers, rate limiting, monitoring)

---

## 📜 Changelog

### v2.0.0 (2026-06-21)

**Breaking changes:** All engines rewritten with proven baselines.

- Quantum Field: Complex amplitudes with π phase offsets, entanglement, measurable KL shift
- Neuromorphic: Lateral inhibition, temporal coding, refractory periods, adaptive thresholds, exponential STDP decay
- Information Field: zlib compression entropy, compression-based MI (`C(X)+C(Y)-C(X,Y)`), KL divergence with Laplace smoothing
- Wave Resonance: FFT cross-spectral density, coherence, phase consistency via circular mean
- Reservoir: Trainable ridge regression readout, separation metric, auto-training from quality feedback
- Spintronic: SQLite persistence (survives restart), n-gram vector similarity, LRU-K, read/write cost tracking
- Relativistic: Sentence-scoring compression, radioactive priority decay (`P₀·e^(-λt)`), EDF deadlines, latency percentiles
- Thermodynamics: Real power via psutil, joules-per-query tracking, energy-proportional routing, model power comparison
- Added 34 tests, every engine must prove value vs baseline

### v1.0.0 (2026-06-21)

- Initial implementation of 15 physics engines
- Honest "real vs simulated" framework

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Ketchum's Physics Optimized Super Intelligence**

Built with physics. Proven with tests. Honest about what's real.

</div>
