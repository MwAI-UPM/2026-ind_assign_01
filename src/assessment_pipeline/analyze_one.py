"""
Analyze a single normalized submission.
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
    ANALYSIS_PROMPT,
)


def main() -> None:
    """Analyze one normalized submission selected by its student ID."""

    if len(sys.argv) != 2:

        print(
            "Usage:"
        )

        print(
            "python analyze_one.py <student_id>"
        )

        raise SystemExit(
            1
        )

    student_id = (
        sys.argv[1]
    )

    submission_file = (
        Path(
            "data/normalized"
        )
        /
        f"{student_id}.json"
    )

    submission = json.loads(
        submission_file.read_text(
            encoding="utf-8",
        )
    )

    MAX_CHARS = 8000

    remaining = MAX_CHARS

    documents = []

    for doc in submission.get(
        "documents",
        []
    ):

        if remaining <= 0:
            break

        text = doc.get(
            "text_content",
            ""
        )[:remaining]

        documents.append(
            {
                "file_name": doc.get(
                    "file_name"
                ),
                "extension": doc.get(
                    "extension"
                ),
                "characters": doc.get(
                    "characters"
                ),
                "text_content": text,
            }
        )

        remaining -= len(
            text
        )

    reduced_payload = {
        "student_id": submission.get(
            "student_id"
        ),
        "student_name": submission.get(
            "student_name"
        ),
        "documents": documents,
    }

    chars_sent = sum(
        len(
            doc["text_content"]
        )
        for doc in reduced_payload[
            "documents"
        ]
    )

    print(
        f"Student: {student_id}"
    )

    print(
        f"Characters sent: {chars_sent}"
    )

    client = GptOssClient(
        host="http://192.168.110.244:11434",
        model="gpt-oss:120b",
    )

    result = run_prompt(
        client=client,
        prompt_template=(
            ANALYSIS_PROMPT
        ),
        payload=reduced_payload,
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
