"""
Evaluate all student analyses.
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
    EVALUATION_PROMPT,
)


ANALYSIS_FOLDER = Path(
    "data/analysis"
)

OUTPUT_FOLDER = Path(
    "data/evaluation"
)


def main() -> None:
    """
    Evaluate all generated analyses.
    """

    client = GptOssClient(
        host="http://192.168.110.244:11434",
        model="gpt-oss:120b",
    )

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    for analysis_file in sorted(
        ANALYSIS_FOLDER.glob(
            "*_analysis.json"
        )
    ):

        student_id = (
            analysis_file.stem
            .replace(
                "_analysis",
                "",
            )
        )

        print(
            f"Evaluating {student_id}"
        )

        try:

            analysis = json.loads(
                analysis_file.read_text(
                    encoding="utf-8",
                )
            )

            evaluation = run_prompt(
                client=client,
                prompt_template=(
                    EVALUATION_PROMPT
                ),
                payload=analysis,
            )

            output_file = (
                OUTPUT_FOLDER
                /
                f"{student_id}_evaluation.json"
            )

            output_file.write_text(
                json.dumps(
                    evaluation,
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
