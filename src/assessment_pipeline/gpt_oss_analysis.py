"""Standalone exploratory GPT-OSS analysis script.

This legacy script demonstrates a direct model request for one fixed input
file.  The maintained batch and single-submission entry points are
``analyze_all`` and ``analyze_one``.
"""

from __future__ import annotations

import json

from pathlib import Path

from assessment_pipeline.gpt_oss_client import (
    GptOssClient,
)

INPUT = Path(
    "data/normalized/80951.json"
)

client = GptOssClient(
    host="http://192.168.110.244:11434",
    model="gpt-oss:120b",
)

data = json.loads(
    INPUT.read_text(
        encoding="utf-8",
    )
)

prompt = f"""
You are a data extraction engine.

You MUST return valid JSON.

Do not use markdown.
Do not use headings.
Do not use prose outside JSON.

Schema:

{{
  "submission_type": "",
  "tasks_detected": [],
  "completeness": "",
  "summary": ""
}}

Submission:

{submission_text}
"""

response = client.generate(
    prompt=prompt
)

print(response)
