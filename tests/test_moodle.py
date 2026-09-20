from pathlib import Path

from assessment_pipeline.moodle import (
    MoodleFolderScanner,
)


def test_folder_pattern() -> None:

    scanner = MoodleFolderScanner()

    discovered = scanner.scan(
        Path(
            "fixtures"
        )
    )

    assert isinstance(
        discovered,
        list,
    )
