"""
Digital Twin adoption report.

Detects Digital Twin proposals directly from
the normalized submissions, not from GPT summaries.

Output:

data/dt_adoption.csv
"""

from __future__ import annotations

import csv
import json

from pathlib import Path


NORMALIZED_FOLDER = Path(
    "data/normalized"
)

ANALYSIS_FOLDER = Path(
    "data/analysis"
)

EVALUATION_FOLDER = Path(
    "data/evaluation"
)

OUTPUT_FILE = Path(
    "data/dt_adoption.csv"
)


DT_TERMS = [
    "digital twin",
    "digital twins",
    "digital-twin",
    "digital-twin system",
    "digital twinning",
]


DT_RECOMMENDATION_PATTERNS = [
    "recommended path",
    "recommend implementing",
    "recommend a digital twin",
    "proposed architecture",
    "proposed blueprint",
    "stand up a digital twin",
    "stand up a digital-twin",
    "adopt a digital twin",
    "deploy a digital twin",
    "digital-twin data backbone",
    "digital twin data backbone",
    "implementation roadmap",
    "phase 1",
]


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


def build_full_text(
    submission: dict,
) -> str:
    """Concatenate the extracted text from all submission documents.

    Args:
        submission: Normalized submission record containing ``documents``.

    Returns:
        Document text joined with blank-line separators.
    """

    parts = []

    for doc in submission.get(
        "documents",
        []
    ):

        parts.append(
            doc.get(
                "text_content",
                ""
            )
        )

    return "\n\n".join(
        parts
    )


def classify_digital_twin(
    full_text: str,
    tasks_completed: int,
) -> tuple[str, str]:
    """Classify Digital Twin adoption using lexical evidence.

    Args:
        full_text: Complete normalized submission text.
        tasks_completed: Number of assignment tasks detected in the analysis.

    Returns:
        A pair containing the status label and a short evidence excerpt.
        Statuses are ``DT_recommended``, ``DT_mentioned``, ``DT_not_found``,
        and ``DT_not_evaluable``.
    """

    if tasks_completed < 4:

        return (
            "DT_not_evaluable",
            "",
        )

    text = full_text.lower()

    mentioned = any(
        keyword in text
        for keyword in DT_TERMS
    )

    if not mentioned:

        return (
            "DT_not_found",
            "",
        )

    for pattern in DT_RECOMMENDATION_PATTERNS:

        idx = text.find(
            pattern
        )

        if idx >= 0:

            start = max(
                0,
                idx - 80,
            )

            end = min(
                len(text),
                idx + 120,
            )

            evidence = (
                full_text[
                    start:end
                ]
                .replace(
                    "\n",
                    " ",
                )
                .strip()
            )

            return (
                "DT_recommended",
                evidence,
            )

    return (
        "DT_mentioned",
        "Digital Twin mentioned",
    )


def main() -> None:
    """Generate the Digital Twin adoption CSV report."""

    rows = []

    counters = {
        "DT_recommended": 0,
        "DT_mentioned": 0,
        "DT_not_found": 0,
        "DT_not_evaluable": 0,
    }

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
            /
            f"{student_id}.json"
        )

        evaluation_file = (
            EVALUATION_FOLDER
            /
            f"{student_id}_evaluation.json"
        )

        if not normalized_file.exists():
            continue

        if not evaluation_file.exists():
            continue

        normalized = load_json(
            normalized_file
        )

        analysis = load_json(
            analysis_file
        )

        evaluation = load_json(
            evaluation_file
        )

        student_name = (
            normalized.get(
                "student_name",
                ""
            )
        )

        tasks_completed = len(
            analysis.get(
                "tasks_detected",
                [],
            )
        )

        full_text = (
           build_full_text(
                normalized
            )
        )

        dt_status, evidence = (
            classify_digital_twin(
                full_text,
                tasks_completed,
            )
        )

        counters[
            dt_status
        ] += 1

        rows.append(
            {
                "student_id":
                    student_id,

                "student_name":
                    student_name,

                "assignment_type":
                    analysis.get(
                        "assignment_type"
                    ),

                "tasks_completed":
                    tasks_completed,

                "quality":
                    evaluation.get(
                        "quality"
                    ),

                "digital_twin":
                    dt_status,

                "dt_evidence":
                    evidence,
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
                "assignment_type",
                "tasks_completed",
                "quality",
                "digital_twin",
                "dt_evidence",
            ],
        )

        writer.writeheader()
        writer.writerows(
            rows
        )

    print(
        f"\nWritten {len(rows)} rows to {OUTPUT_FILE}"
    )

    print()

    for key, value in (
        counters.items()
    ):

        print(
            f"{key}: {value}"
        )


if __name__ == "__main__":
    main()
