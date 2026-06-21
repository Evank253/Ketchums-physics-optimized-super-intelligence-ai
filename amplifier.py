"""
Ketchum's Physics Optimized Super Intelligence
Response Amplifier — v2
"""

from typing import Optional


def strengthen_response(response: str, query_type: str) -> str:
    if not response or len(response) < 20:
        return response

    amplified = response

    if query_type == "coding":
        lines = amplified.split("\n")
        has_code_block = "```" in amplified
        has_indented_code = any(line.startswith("    ") or line.startswith("\t") for line in lines)
        if has_indented_code and not has_code_block:
            amplified = "```\n" + amplified + "\n```"

    elif query_type == "math":
        if "step" not in amplified.lower() and len(amplified) > 200:
            amplified = "**Solution:**\n\n" + amplified

    elif query_type == "planning":
        if not any(marker in amplified for marker in ["1.", "Step", "- "]):
            amplified = "- " + amplified

    elif query_type == "reasoning":
        if "therefore" not in amplified.lower() and "thus" not in amplified.lower():
            if len(amplified) > 100:
                amplified += "\n\nTherefore, the reasoning above supports the conclusion."

    elif query_type == "analysis":
        if len(amplified) > 500 and "summary" not in amplified.lower():
            amplified += "\n\n**Summary:** The analysis above covers the key points of comparison."

    return amplified
