"""
LLM analysis utilities.
"""

from __future__ import annotations

import json

from assessment_pipeline.gpt_oss_client import (
    GptOssClient,
)


def run_prompt(
    client: GptOssClient,
    prompt_template: str,
    payload: dict,
) -> dict:
    """Send a structured payload to an LLM and parse its JSON response.

    Args:
        client: Configured GPT-OSS client used to generate the response.
        prompt_template: Instruction text prepended to the serialized payload.
        payload: JSON-serializable submission or analysis data.

    Returns:
        The decoded JSON object returned by the model.

    Raises:
        ValueError: If the model returns an empty response.
        json.JSONDecodeError: If the response is not valid JSON.
    """

    prompt = (
        prompt_template
        + "\n\nSubmission:\n\n"
        + json.dumps(
            payload,
            ensure_ascii=False,
        )
    )

    response = client.generate(
        prompt
    )

    if not response:
        raise ValueError(
            "Empty model request"
        )

    if response.startswith(
        "```json"
    ):
        response = (
            response
            .replace(
                "```json",
                "",
            )
            .replace(
                "```",
                "",
            )
            .strip()
        )
    try:
        return json.loads(
            response
        )

    except Exception as exc:
        print(
            "INVALID RESPONSE"
        )

        print(
            f"JSON ERROR: {exc}"
        )

        print(
            "RAW RESPONSE START:",
        )

        print(
            response[:2000]
        )

        print(
            "RAW RESPONSE END.",
        )
        raise
