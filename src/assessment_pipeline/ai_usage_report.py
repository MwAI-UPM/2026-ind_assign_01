"""
Generate AI usage report.

Output:
data/ai_usage_report.csv
"""

from __future__ import annotations

import csv
import json

from pathlib import Path


ANALYSIS_FOLDER = Path(
    "data/analysis"
)

NORMALIZED_FOLDER = Path(
    "data/normalized"
)

OUTPUT_FILE = Path(
    "data/ai_usage_report.csv"
)


def load_json(
    path: Path,
) -> dict:
    """Load a UTF-8 encoded JSON object from disk.

    Args:
        path: JSON file to read.

    Returns:
        Decoded JSON object.
    """

    return json.loads(
        path.read_text(
            encoding="utf-8",
        )
    )


def get_student_name(
    normalized: dict,
) -> str:
    """Extract the student name from a normalized submission record.

    Args:
        normalized: Normalized submission data.

    Returns:
        Student name, or an empty string when it is unavailable.
    """

    return normalized.get(
        "student_name",
        ""
    )


def main() -> None:
    """Generate the cohort-level AI usage CSV report."""

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

        normalized_file = (
            NORMALIZED_FOLDER
            / f"{student_id}.json"
        )

        analysis = load_json(
            analysis_file
        )

        student_name = ""

        if normalized_file.exists():

            normalized = load_json(
                normalized_file
            )

            student_name = (
                get_student_name(
                    normalized
                )
            )

        rows.append(
            {
                "student_id":
                    student_id,

                "student_name":
                    student_name,

                "completeness":
                    analysis.get(
                        "completeness",
                        "",
                    ),

                "ai_usage_declared":
                    analysis.get(
                        "ai_usage_declared",
                        False,
                    ),

                "ai_tools":
                    "; ".join(
                        analysis.get(
                            "ai_tools_mentioned",
                            [],
                        )
                    ),

                "ai_usage_evidence":
                    " | ".join(
                        analysis.get(
                            "ai_usage_evidence",
                            [],
                        )
                    ),
            }
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
                "student_name",
                "completeness",
                "ai_usage_declared",
                "ai_tools",
                "ai_usage_evidence",
            ],
        )

        writer.writeheader()
        writer.writerows(
            rows
        )

    print(
        f"Written {len(rows)} rows to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
