"""
Batch processing of Moodle submissions.
"""

from __future__ import annotations

from pathlib import Path

from assessment_pipeline.reporting import (
    CsvReporter,
)
from assessment_pipeline.extractor import (
    SubmissionExtractor,
)
from assessment_pipeline.moodle import (
    MoodleFolderScanner,
)
from assessment_pipeline.normalizer import (
    JsonNormalizer,
)


ROOT = Path(
    "/media/samba/docencia/UPM/Masters/MIO_AIM/2627/practicas/Assignment_Class_01"
)

OUTPUT_DIR = Path(
    "data/normalized"
)


def main() -> None:
    """
    Process all Moodle submissions.
    """

    reporter = CsvReporter()
    processed_submissions = []

    scanner = MoodleFolderScanner()

    extractor = SubmissionExtractor()

    normalizer = JsonNormalizer()

    submissions = scanner.scan(ROOT)

    print()
    print(
        f"Students discovered: {len(submissions)}"
    )
    print()

    for student_name, student_id, folder in submissions:

        print(
            f"Processing {student_id} "
            f"| {student_name}"
        )

        try:
            submission = extractor.extract(
                student_name=student_name,
                student_id=student_id,
                submission_folder=folder,
            )

            total_section_characters = sum(
                section.characters
                for section in submission.task_sections
            )

            output_path = (
                OUTPUT_DIR /
                f"{student_id}.json"
            )

            normalizer.write(
                submission,
                output_path,
            )

            processed_submissions.append(
                submission
            )

            print(
                f"  Documents: "
                f"{submission.total_documents}"
            )

            print(
                f"  Characters: "
                f"{submission.total_characters}"
            )

            print(
                f"  Task sections: "
                f"{len(submission.task_sections)}"
            )

            for section in submission.task_sections:
                print(
                   f" Task {section.task_number}: "
                   f"{section.characters}"
            )

            print(
                f"  Section chars: "
                f"{total_section_characters}"
            )

            print(
                f"  Coverage: "
                f"{submission.section_coverage:.1%}"
            )

        except Exception as exc:

            print(
                f"  ERROR: {exc}"
            )

    reporter.write(
        submissions=processed_submissions,
        output_path=Path(
            "data/reports/submissions.csv"
        ),
    )

    print()
    print("Processing completed.")


if __name__ == "__main__":

    main()
