"""
Build a cohort summary CSV from analysis and evaluation results.
"""

from __future__ import annotations

import csv
import json

from collections import Counter
from pathlib import Path


ANALYSIS_FOLDER = Path(
    "data/analysis"
)

EVALUATION_FOLDER = Path(
    "data/evaluation"
)

OUTPUT_FILE = Path(
    "data/cohort_summary.csv"
)


def main() -> None:
    """Build the cohort summary CSV from matching analysis and evaluation files."""

    rows = []

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

        evaluation_file = (
            EVALUATION_FOLDER
            / f"{student_id}_evaluation.json"
        )

        if not evaluation_file.exists():
            continue

        analysis = json.loads(
            analysis_file.read_text(
                encoding="utf-8",
            )
        )

        evaluation = json.loads(
            evaluation_file.read_text(
                encoding="utf-8",
            )
        )

        rows.append(
            {
                "student_id": student_id,
                "assignment_type": analysis.get(
                    "assignment_type"
                ),
                "tasks_detected": len(
                    analysis.get(
                        "tasks_detected",
                        [],
                    )
                ),
                "analysis_completeness": analysis.get(
                    "completeness"
                ),
                "evaluation_completeness": evaluation.get(
                    "completeness"
                ),
                "quality": evaluation.get(
                    "quality"
                ),
                "evidence_strength": evaluation.get(
                    "evidence_strength"
                ),
                "confidence": evaluation.get(
                    "confidence"
                ),
                "ai_usage_declared":
                    analysis.get(
                        "ai_usage_declared"
                    ),

                "ai_tools_count":
                    len(
                        analysis.get(
                            "ai_tools_mentioned",
                            [],
                        )
                    ),
                "ai_tools":
                    ";".join(
                        analysis.get(
                            "ai_tools_mentioned",
                            [],
                        )
                    ),
            }
        )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csvfile:

        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                "student_id",
                "assignment_type",
                "tasks_detected",
                "analysis_completeness",
                "evaluation_completeness",
                "quality",
                "evidence_strength",
                "confidence",
            ],
        )

        writer.writeheader()
        writer.writerows(
            rows
        )

    print(
        f"Written {len(rows)} rows to {OUTPUT_FILE}"
    )

    print("\nQUALITY")

    for key, value in Counter(
        row["quality"]
        for row in rows
    ).items():

        print(
            f"{key}: {value}"
        )

    print("\nCOMPLETENESS")

    for key, value in Counter(
        row["evaluation_completeness"]
        for row in rows
    ).items():

        print(
            f"{key}: {value}"
        )


if __name__ == "__main__":
    main()
