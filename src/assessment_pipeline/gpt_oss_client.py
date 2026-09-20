"""
GPT-OSS client using a remote Ollama server.
"""

from __future__ import annotations

import requests


class GptOssClient:
    """
    Thin wrapper around the Ollama REST API.
    """

    def __init__(
        self,
        host: str,
        model: str,
    ) -> None:
        """
        Initialize client.

        Args:
            host:
                Ollama base URL.

            model:
                Ollama model name.
        """

        self.host = host.rstrip("/")
        self.model = model

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response.

        Args:
            prompt:
                Prompt sent to the model.

        Returns:
            Model response text.
        """

        response = requests.post(
            f"{self.host}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=1800,
        )

        response.raise_for_status()

        payload = response.json()

        return payload["response"]
