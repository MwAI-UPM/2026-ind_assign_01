"""
Evaluate a single analysis.
"""

from __future__ import annotations

import json
import sys

from pathlib import Path

from assessment_pipeline.gpt_oss_client import (
    GptOssClient,
)

from assessment_pipeline.llm_pipeline import (
    run_prompt,
)

from assessment_pipeline.prompts import (
    EVALUATION_PROMPT,
)


def main() -> None:
    """Evaluate one previously generated analysis by student ID."""

    if len(sys.argv) != 2:

        print(
            "Usage:"
        )

        print(
            "python evaluate_one.py <student_id>"
        )

        raise SystemExit(
            1
        )

    student_id = (
        sys.argv[1]
    )

    analysis_file = (
        Path(
            "data/analysis"
        )
        /
        f"{student_id}_analysis.json"
    )

    analysis = json.loads(
        analysis_file.read_text(
            encoding="utf-8",
        )
    )

    print(
        f"Student: {student_id}"
    )

    client = GptOssClient(
        host="http://192.168.110.244:11434",
        model="gpt-oss:120b",
    )

    result = run_prompt(
        client=client,
        prompt_template=(
            EVALUATION_PROMPT
        ),
        payload=analysis,
    )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
