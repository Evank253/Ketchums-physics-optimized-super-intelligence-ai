"""
Ketchum's Physics Optimized Super Intelligence
Unified Engine — v2

Full pipeline integration with all 15 physics engines.
Tracks energy, deadline compliance, and training state.
"""

import time
from typing import Optional

from core.physics.master_optimizer import MasterPhysicsOptimizer
from core.intelligence.scorer import score_response, pick_best_response
from core.intelligence.amplifier import strengthen_response
from core.memory.store import retrieve, add


class UnifiedSuperIntelligence:

    def __init__(self, spintronic_db_path: str = ".spintronic.db"):
        self.guardian = None
        self.sii = None
        self.model_strengths = {
            "coding": ["gpt-4-turbo", "claude-3-opus"],
            "reasoning": ["claude-3-opus", "gpt-4-turbo"],
            "research": ["gemini-pro", "gpt-4-turbo"],
            "creative": ["claude-3-opus", "claude-3-sonnet"],
            "math": ["gpt-4-turbo", "gemini-pro"],
            "planning": ["gpt-4-turbo", "claude-3-sonnet"],
            "analysis": ["claude-3-opus", "gpt-4-turbo"],
            "general": ["claude-3-sonnet", "gpt-4-turbo"],
        }
        self._query_model = None
        self.physics = MasterPhysicsOptimizer(spintronic_db_path=spintronic_db_path)

    def set_model_query(self, query_fn):
        self._query_model = query_fn

    def set_guardian(self, guardian):
        self.guardian = guardian

    def set_sii(self, sii):
        self.sii = sii

    def check_shutdown(self) -> bool:
        return False

    async def _query_model_async(self, prompt: str, model: str) -> str:
        if self._query_model:
            return await self._query_model(prompt, model)
        return f"[Response from {model}]"

    def _build_prompt(self, optimized: str, context: str) -> str:
        if context:
            return f"{context}\n\nQuery: {optimized}"
        return optimized

    def _offline_response(self) -> dict:
        return {"response": "System is currently offline. Please try again later.", "safe": True, "offline": True}

    def _blocked_response(self, reason: str) -> dict:
        return {"response": f"Request could not be processed: {reason}", "safe": True, "blocked": True}

    async def process(self, prompt: str, user_id: str = "default", mode: str = "auto") -> dict:
        start_time = time.time()

        if self.guardian:
            try:
                if self.check_shutdown():
                    return self._offline_response()
                pre_check = await self.guardian.pre_flight(prompt, user_id)
                if not pre_check.get("safe", True):
                    return self._blocked_response(pre_check.get("reason", "Blocked"))
            except Exception:
                pass

        pre = await self.physics.pre_process(prompt)

        if pre["cached_response"]:
            cached = pre["cached_response"]
            if isinstance(cached, dict) and "response" in cached:
                return {**cached, "served_from_cache": True,
                        "physics_pre": {"thermal_state": pre["thermal_state"],
                                        "pre_process_ms": pre["pre_process_ms"]}}

        query_type = pre["query_type"]
        primary_model = pre["model_selected"]
        optimized = pre["optimized_prompt"]

        memory_context = retrieve(prompt)
        sii_context = ""
        if self.sii:
            try:
                sii_context = self.sii.get_enhanced_context(prompt)
            except Exception:
                pass

        physics_ctx = ""
        if pre["physics_context"]:
            physics_ctx = "Physics constants: " + " | ".join(f"{k}={v}" for k, v in pre["physics_context"].items())

        full_context = "\n".join(filter(None, [physics_ctx, sii_context, memory_context or ""]))
        enriched = self._build_prompt(optimized, full_context)

        models = [primary_model]
        for m in self.model_strengths.get(query_type, []):
            if m != primary_model and len(models) < 3:
                models.append(m)

        photonic_result = await self.physics.execute_parallel(enriched, models, self._query_model_async)
        responses = photonic_result["responses"]

        if not responses:
            try:
                fallback = await self._query_model_async(enriched, primary_model)
                responses = [fallback] if fallback else [""]
            except Exception:
                responses = [""]

        best = pick_best_response(responses, query_type)
        post = await self.physics.post_process(
            prompt=prompt, responses=responses, best=best,
            query_type=query_type, model_used=primary_model,
            start_time=start_time, deadline_ms=pre.get("deadline_ms", 5000.0),
        )
        final_response = post["response"]

        if self.sii:
            try:
                await self.sii.process_and_learn(
                    prompt, final_response, user_id, query_type,
                    post["physics_metrics"]["quality_score"],
                )
            except Exception:
                pass

        if self.guardian:
            try:
                post_check = await self.guardian.post_flight(final_response, user_id)
                if not post_check.get("safe", True):
                    return self._blocked_response("Filtered")
            except Exception:
                pass

        final = strengthen_response(final_response, query_type)
        add(prompt)

        return {
            "response": final, "model_used": primary_model,
            "query_type": query_type, "safe": True,
            "physics": post["physics_metrics"],
            "quantum": {
                "intent_probability": pre["quantum_prob"],
                "spike_confidence": pre["spike_confidence"],
                "uncertainty": pre["uncertainty"],
                "interference_shift": pre.get("interference_shift", 0),
                "boltzmann_prob": pre["boltzmann_prob"],
            },
            "performance": {
                "latency_ms": post["physics_metrics"]["latency_ms"],
                "met_deadline": post["physics_metrics"].get("met_deadline", True),
                "thermal_state": pre["thermal_state"],
                "thermal_efficiency": pre["thermal_efficiency"],
                "energy_joules": post["physics_metrics"].get("energy_joules", 0),
                "photonic_speedup": photonic_result.get("speedup", 1.0),
                "pre_process_ms": pre["pre_process_ms"],
                "cache_hit": False,
                "contraction_method": pre.get("contraction_method", "unknown"),
                "reservoir_trained": post["physics_metrics"].get("reservoir_trained", False),
            },
        }

    def get_physics_report(self) -> dict:
        return self.physics.get_full_report()

    def cleanup(self):
        try:
            self.physics.spintronic.close()
        except Exception:
            pass
