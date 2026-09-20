# tests/test_archives.py
from pathlib import Path

from assessment_pipeline.moodle import (
    MoodleFolderScanner,
)

from assessment_pipeline.utils.archive import (
    ArchiveExtractor,
)

ROOT = Path(
    "/media/samba/docencia/UPM/Masters/MIO_AIM/2627/practicas/Assignment_Class_01"
)

scanner = MoodleFolderScanner()
extractor = ArchiveExtractor()

total = 0

for _, student_id, folder in scanner.scan(ROOT):

    extracted = extractor.extract_recursive(
        folder
    )

    total += len(extracted)

    print(
        f"{student_id}: {len(extracted)}"
    )

print()
print(
    f"Total extracted directories: {total}"
)
