"""
Ketchum's Physics Optimized Super Intelligence
Quantum Compression Engine — v2

PHYSICS:
- Amplitude encoding: normalize to unit vector (quantum state)
- SVD for low-rank approximation
- FFT spectral compression
- Fidelity = cosine similarity between original and reconstructed
"""

import math
import numpy as np
from typing import Optional


class QuantumCompressionEngine:

    def __init__(self):
        self.compression_stats = {"compressions": 0, "avg_ratio": 0.0, "avg_fidelity": 0.0}

    def compress_text(self, text: str) -> dict:
        self.compression_stats["compressions"] += 1
        if not text or len(text) < 5:
            return {"ratio": 0.0, "method": "passthrough", "original_size": len(text)}

        original_size = len(text)
        signal = np.array([ord(c) for c in text], dtype=np.float64)
        norm = np.linalg.norm(signal)
        if norm == 0:
            return {"ratio": 0.0, "method": "zero_signal", "original_size": original_size}

        amplitudes = signal / norm
        spectrum = np.fft.fft(amplitudes)
        magnitudes = np.abs(spectrum)
        max_mag = np.max(magnitudes)
        if max_mag == 0:
            return {"ratio": 0.0, "method": "zero_spectrum", "original_size": original_size}

        threshold = max_mag * 0.01
        compressed_spectrum = np.where(magnitudes > threshold, spectrum, 0.0 + 0.0j)
        nonzero = np.count_nonzero(compressed_spectrum)
        ratio = 1.0 - (nonzero / len(spectrum))

        reconstructed_amplitudes = np.fft.ifft(compressed_spectrum)
        fidelity = float(np.real(np.dot(amplitudes, np.conj(reconstructed_amplitudes))) ** 2)
        fidelity = min(fidelity, 1.0)

        n = self.compression_stats["compressions"]
        self.compression_stats["avg_ratio"] = round((self.compression_stats["avg_ratio"] * (n - 1) + ratio) / n, 4)
        self.compression_stats["avg_fidelity"] = round((self.compression_stats["avg_fidelity"] * (n - 1) + fidelity) / n, 4)

        return {
            "ratio": round(ratio, 4), "fidelity": round(fidelity, 6),
            "original_size": original_size, "compressed_size": nonzero,
            "method": "quantum_amplitude_fft",
        }

    def compress_embedding(self, embedding: list, target_rank: int = 32) -> dict:
        arr = np.array(embedding, dtype=np.float64)
        norm = np.linalg.norm(arr)
        if norm == 0:
            return {"ratio": 0.0, "fidelity": 0.0}

        dim = len(arr)
        rows = int(math.sqrt(dim))
        cols = dim // rows
        if rows * cols < dim:
            rows += 1

        padded = np.zeros(rows * cols)
        padded[:dim] = arr
        matrix = padded.reshape(rows, cols)

        U, S, Vt = np.linalg.svd(matrix, full_matrices=False)
        rank = min(target_rank, len(S))
        U_r, S_r, Vt_r = U[:, :rank], S[:rank], Vt[:rank, :]

        total_energy = np.sum(S ** 2)
        retained_energy = np.sum(S_r ** 2)
        fidelity = retained_energy / max(total_energy, 1e-10)

        compressed_size = rank * (rows + cols + 1)
        ratio = 1.0 - (compressed_size / dim)

        return {
            "ratio": round(ratio, 4), "fidelity": round(fidelity, 6),
            "rank": rank, "original_dim": dim, "compressed_size": compressed_size,
        }

    def get_compression_stats(self) -> dict:
        return self.compression_stats
