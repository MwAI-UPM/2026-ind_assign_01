"""
Explicit AI tool detection.
"""

from __future__ import annotations

import re


AI_PATTERNS = {
    "ChatGPT": [
        r"\bchatgpt\b",
        r"\bgpt-4\b",
        r"\bgpt4\b",
    ],
    "Claude": [
        r"\bclaude\b",
    ],
    "Copilot": [
        r"\bcopilot\b",
        r"\bmicrosoft copilot\b",
        r"\bgithub copilot\b",
    ],
    "Gemini": [
        r"\bgemini\b",
        r"\bgoogle gemini\b",
        r"\bbard\b",
    ],
    "Perplexity": [
        r"\bperplexity\b",
    ],
    "LLM": [
        r"\blarge language model\b",
        r"\bllm\b",
        r"\bgenerative ai\b",
        r"\bartificial intelligence\b",
    ],
}


def detect_ai_tools(text: str) -> list[str]:
    """Detect explicit AI-tool mentions in submission text.

    Args:
        text: Text to scan case-insensitively using the configured patterns.

    Returns:
        Sorted, de-duplicated labels for the AI tools or concepts detected.

    Note:
        This is lexical mention detection, not authorship attribution or
        evidence that a tool was actually used.
    """

    text = text.lower()

    detected = []

    for tool_name, patterns in AI_PATTERNS.items():

        for pattern in patterns:

            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            ):

                detected.append(
                    tool_name
                )

                break

    return sorted(
        set(detected)
    )
