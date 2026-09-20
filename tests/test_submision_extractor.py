from pathlib import Path

from assessment_pipeline.extractor import (
    SubmissionExtractor,
)

extractor = SubmissionExtractor()

submission = extractor.extract(
    student_name="GOÑI OTAZU MIKEL",
    student_id="80964",
    submission_folder=Path(
        "../GOÑI OTAZU MIKEL_80964_assignsubmission_file"
    ),
)

print()
print("Student:", submission.student_name)

print(
    "Documents:",
    submission.total_documents,
)

print(
    "Characters:",
    submission.total_characters,
)

print()

for document in submission.documents:

    print(
        document.task_number,
        document.file_name,
        document.characters,
    )
