"""
Moodle export discovery utilities.
"""

import re
from pathlib import Path


class MoodleFolderScanner:
    """
    Discover Moodle submission folders.

    Moodle exports commonly generate folder names
    following the pattern::

        STUDENT_NAME_ID_assignsubmission_file

    Example::

        GOÑI OTAZU MIKEL_80964_assignsubmission_file
    """

    PATTERN = re.compile(
        r"^(.*?)_(\d+)_assignsubmission_file$"
    )

    def scan(
        self,
        root: Path,
    ) -> list[tuple[str, str, Path]]:
        """
        Scan a Moodle export directory.

        Args:
            root:
                Directory containing Moodle exports.

        Returns:
            List of tuples containing:

            - student name
            - student identifier
            - submission path
        """

        discovered = []

        for path in root.iterdir():

            if not path.is_dir():
                continue

            match = self.PATTERN.match(path.name)

            if not match:
                continue

            discovered.append(
                (
                    match.group(1),
                    match.group(2),
                    path,
                )
            )

        return discovered
