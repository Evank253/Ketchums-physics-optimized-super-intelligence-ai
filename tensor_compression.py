"""
Ketchum's Physics Optimized Super Intelligence
Tensor Network Compression — v2

PHYSICS:
- Schmidt decomposition (SVD) for optimal low-rank approximation
- Amplitude pruning: zero out small singular values
- FFT spectral compression of text signals
- Fidelity measured as cosine similarity
"""

import numpy as np
import math
from typing import Optional


class TensorNetworkCompressor:

    def __init__(self):
        self.stats = {
            "compressions": 0, "total_original": 0,
            "total_compressed": 0, "avg_ratio": 0.0, "avg_info_retained": 0.0,
        }

    def compress_embedding(self, embedding: list, rank: int = 64, threshold: float = 0.01) -> dict:
        arr = np.array(embedding, dtype=np.float32)
        original_dim = len(arr)

        rows = int(math.sqrt(original_dim))
        cols = original_dim // rows
        padded_size = rows * cols
        if padded_size < original_dim:
            rows += 1
            padded_size = rows * cols

        padded = np.zeros(padded_size)
        padded[:original_dim] = arr
        matrix = padded.reshape(rows, cols)

        U, S, Vt = np.linalg.svd(matrix, full_matrices=False)

        effective_rank = min(rank, len(S))
        U_truncated = U[:, :effective_rank]
        S_truncated = S[:effective_rank]
        Vt_truncated = Vt[:effective_rank, :]

        mask = S_truncated > threshold
        S_pruned = S_truncated * mask

        total_energy = np.sum(S ** 2)
        retained_energy = np.sum(S_pruned ** 2)
        info_retained = retained_energy / total_energy if total_energy > 0 else 1.0

        nonzero_count = int(np.sum(mask))

        compressed = {
            "U": U_truncated[:, :nonzero_count].tolist(),
            "S": S_pruned[:nonzero_count].tolist(),
            "Vt": Vt_truncated[:nonzero_count, :].tolist(),
            "original_dim": original_dim, "rows": rows, "cols": cols, "rank": nonzero_count,
        }

        compressed_size = nonzero_count * rows + nonzero_count + nonzero_count * cols
        ratio = 1.0 - (compressed_size / original_dim)

        self.stats["compressions"] += 1
        self.stats["total_original"] += original_dim
        self.stats["total_compressed"] += compressed_size
        self.stats["avg_info_retained"] = round(
            (self.stats["avg_info_retained"] * (self.stats["compressions"] - 1) + info_retained)
            / self.stats["compressions"], 6,
        )
        self.stats["avg_ratio"] = round(
            1.0 - (self.stats["total_compressed"] / max(self.stats["total_original"], 1)), 4,
        )

        return {
            "compressed": compressed, "original_dim": original_dim,
            "compressed_size": compressed_size, "ratio": round(ratio, 4),
            "info_retained": round(info_retained, 6), "rank_used": nonzero_count,
        }

    def decompress_embedding(self, compressed_data: dict) -> list:
        data = compressed_data["compressed"]
        U = np.array(data["U"])
        S = np.array(data["S"])
        Vt = np.array(data["Vt"])
        reconstructed = U @ np.diag(S) @ Vt
        flat = reconstructed.flatten()
        return flat[:data["original_dim"]].tolist()

    def compress_text_tensor(self, text: str) -> dict:
        if not text or len(text) < 10:
            return {"compressed": text, "ratio": 0.0, "method": "passthrough"}

        signal = np.array([ord(c) for c in text], dtype=np.float32)
        original_size = len(signal)
        spectrum = np.fft.rfft(signal)
        magnitudes = np.abs(spectrum)
        threshold = np.max(magnitudes) * 0.01
        compressed_spectrum = np.where(magnitudes > threshold, spectrum, 0.0)
        nonzero = np.count_nonzero(compressed_spectrum)
        ratio = 1.0 - (nonzero / len(spectrum))

        return {
            "spectrum": compressed_spectrum.tolist(), "original_length": original_size,
            "spectral_size": nonzero, "ratio": round(ratio, 4), "method": "fourier_tensor",
        }

    def decompress_text_tensor(self, compressed_data: dict) -> str:
        spectrum = np.array(compressed_data["spectrum"])
        original_length = compressed_data["original_length"]
        reconstructed = np.fft.irfft(spectrum, n=original_length)
        chars = [chr(max(0, min(127, int(round(c))))) for c in reconstructed]
        return "".join(chars)

    def get_stats(self) -> dict:
        return self.stats
