# test_scan.py

from pathlib import Path

from assessment_pipeline.moodle import (
    MoodleFolderScanner,
)

ROOT = Path(
    "/media/samba/docencia/UPM/Masters/MIO_AIM/2627/practicas/Assignment_Class_01"
)

scanner = MoodleFolderScanner()

submissions = scanner.scan(ROOT)

print(f"Students found: {len(submissions)}")

for name, student_id, folder in submissions[:5]:
    print( f"{student_id} | {name} | {folder.name}")
