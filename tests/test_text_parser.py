from pathlib import Path

from assessment_pipeline.moodle import (
    MoodleFolderScanner,
)
from assessment_pipeline.parsers.text_parser import (
    TextParser,
)

ROOT = Path(
    "/media/samba/docencia/UPM/Masters/MIO_AIM/2627/practicas/Assignment_Class_01"
)

parser = TextParser()

scanner = MoodleFolderScanner()

for _, _, folder in scanner.scan(ROOT):

    for candidate in folder.rglob("*"):

        if candidate.suffix.lower() not in {
            ".txt",
            ".csv",
            ".md",
            ".html",
        }:
            continue

        print()
        print(candidate)

        text = parser.extract_text(candidate)

        print(
            f"Characters: {len(text)}"
        )

        print()
        print(text[:500])

        raise SystemExit(0)

print("No supported text files found.")
