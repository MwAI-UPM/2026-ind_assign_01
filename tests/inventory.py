from collections import Counter
from pathlib import Path

from assessment_pipeline.moodle import (
    MoodleFolderScanner,
)

ROOT = Path(
    "/media/samba/docencia/UPM/Masters/MIO_AIM/2627/practicas/Assignment_Class_01"
)

counter = Counter()

scanner = MoodleFolderScanner()

for _, _, folder in scanner.scan(ROOT):

    for path in folder.rglob("*"):

        if path.is_file():
            counter[path.suffix.lower()] += 1

print()

for ext, count in sorted(counter.items()):
    print(
        f"{ext or '[no extension]'} : {count}"
    )

print()
print(
    f"TOTAL FILES: {sum(counter.values())}"
)
