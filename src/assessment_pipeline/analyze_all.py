"""
Analyze all normalized submissions.
"""

from __future__ import annotations

import json

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

from assessment_pipeline.ai_detection import (
    detect_ai_tools,
)


INPUT_FOLDER = Path(
    "data/normalized"
)

OUTPUT_FOLDER = Path(
    "data/analysis"
)


MAX_CHARS = 8000


def main() -> None:
    """
    Analyze all normalized submissions.
    """

    client = GptOssClient(
        host="http://192.168.110.244:11434",
        model="gpt-oss:120b",
    )

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    for submission_file in sorted(
        INPUT_FOLDER.glob(
            "*.json"
        )
    ):

        student_id = (
            submission_file.stem
        )

        print(
            f"Analyzing {student_id}"
        )

        try:

            submission = json.loads(
                submission_file.read_text(
                    encoding="utf-8",
                )
            )

            remaining = MAX_CHARS

            documents = []

            #
            # Full text for deterministic
            # AI-tool detection
            #
            full_text = ""

            for doc in submission.get(
                "documents",
                []
            ):

                doc_text = doc.get(
                    "text_content",
                    ""
                )

                #
                # Build complete corpus
                # (untruncated)
                #
                full_text += (
                    "\n\n" + doc_text
                )

                #
                # Build reduced payload
                # for GPT
                #
                if remaining <= 0:
                    continue

                reduced_text = (
                    doc_text[:remaining]
                )

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
                        "text_content": reduced_text,
                    }
                )

                remaining -= len(
                    reduced_text
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
                    d["text_content"]
                )
                for d in documents
            )

            print(
                student_id,
                chars_sent,
            )

            result = run_prompt(
                client=client,
                prompt_template=(
                    ANALYSIS_PROMPT
                ),
                payload=reduced_payload,
            )

            #
            # Deterministic AI detection
            #
            ai_tools = detect_ai_tools(
                full_text
            )

            result[
                "ai_usage_declared"
            ] = (
                len(ai_tools) > 0
            )

            result[
                "ai_tools_mentioned"
            ] = ai_tools

            result[
                "ai_detection_method"
            ] = (
                "keyword_search"
            )

            output_file = (
                OUTPUT_FOLDER
                /
                f"{student_id}_analysis.json"
            )

            output_file.write_text(
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

        except Exception as exc:

            print(
                f"ERROR {student_id}: "
                f"{exc}"
            )


if __name__ == "__main__":
    main()
