from pathlib import Path

from assessment_pipeline.extractor import (
    SubmissionExtractor,
)
from assessment_pipeline.normalizer import (
    JsonNormalizer,
)

submission = SubmissionExtractor().extract(
    student_name="GOÑI OTAZU MIKEL",
    student_id="80964",
    submission_folder=Path(
        "../GOÑI OTAZU MIKEL_80964_assignsubmission_file"
    ),
)

output = Path(
    "data/normalized/80964.json"
)

JsonNormalizer().write(
    submission,
    output,
)

print(
    f"Generated: {output}"
)
