"""
Reporting utilities.
"""

from __future__ import annotations

import csv
from pathlib import Path

from assessment_pipeline.models import (
    StudentSubmission,
)

from assessment_pipeline.content_task_detector import (
    ContentTaskDetector,
)

class CsvReporter:
    """
    Generate control reports from student submissions.
    """

    TASKS = (1, 2, 3, 4, 5)

    def write(
        self,
        submissions: list[StudentSubmission],
        output_path: Path,
    ) -> None:
        """
        Write a CSV control report.

        Args:
            submissions:
                Processed submissions.

            output_path:
                Target CSV file.
        """

        detector = ContentTaskDetector()

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output_path.open(
            mode="w",
            newline="",
            encoding="utf-8",
        ) as handle:

            writer = csv.writer(handle)

            writer.writerow(
                [
                    "student_id",
                    "student_name",
                    "documents",
                    "characters",
                    "detected_tasks",
                    "content_tasks",
                    "auxiliary_documents",
                    "task_sections",
                    "section_characters",
                    "section_coverage",
                    "valid_split",
                    "task_1",
                    "task_2",
                    "task_3",
                    "task_4",
                    "task_5",
                ]
            )

            for submission in submissions:

                task_counts = {
                    task: 0
                    for task in self.TASKS
                }

                detected_tasks = set()
                content_tasks = set()
                auxiliary_documents = 0
                section_characters = 0


                for document in submission.documents:

                    content_tasks.update(
                        detector.detect_tasks(
                            document.text_content
                        )
                    )

                    if document.task_number is None:
                        auxiliary_documents += 1
                        continue

                    detected_tasks.add(
                        document.task_number
                    )

                    task_counts[
                        document.task_number
                    ] += document.characters

                    section_characters = sum(
                        section.characters
                        for section in submission.task_sections
                    )

                    section_coverage = (
                        section_characters
                        / submission.total_characters
                        if submission.total_characters > 0
                        else 0.0
                    )

                    valid_split = (
                        len(submission.task_sections) >= 1
                        and section_coverage >= 0.75
                    )

                writer.writerow(
                    [
                        submission.student_id,
                        submission.student_name,
                        submission.total_documents,
                        submission.total_characters,
                        len(detected_tasks),
                        len(content_tasks),
                        auxiliary_documents,
                        len(submission.task_sections),
                        section_characters,
                        round(
                            section_coverage, 3,
                        ),
                        valid_split,
                        task_counts[1],
                        task_counts[2],
                        task_counts[3],
                        task_counts[4],
                        task_counts[5],
                    ]
                )
