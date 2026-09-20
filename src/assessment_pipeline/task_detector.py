"""
Task identification utilities.

This module provides helper functions to infer
assignment task identifiers from document names.
"""

from __future__ import annotations

import re
from pathlib import Path


class TaskDetector:
    """
    Detect assignment task numbers from file names.

    Examples:
        Task 1 Report.pdf -> 1
        TASK1.docx -> 1
        Task_02_Map.pdf -> 2
        T3_Report.docx -> 3
    """

    TASK_PATTERNS = [
        re.compile(
            r"task[\s_-]*(\d+)",
            flags=re.IGNORECASE,
        ),
        re.compile(
            r"\bt[\s_-]*(\d+)\b",
            flags=re.IGNORECASE,
        ),
    ]

    def detect(
        self,
        file_path: Path,
    ) -> int | None:
        """
        Detect the task number associated with a file.

        Args:
            file_path:
                Document path.

        Returns:
            Task number if detected, otherwise None.
        """

        filename = file_path.stem

        for pattern in self.TASK_PATTERNS:

            match = pattern.search(filename)

            if match is None:
                continue

            try:
                return int(match.group(1))

            except ValueError:
                continue

        return None

    def has_task(
        self,
        file_path: Path,
    ) -> bool:
        """
        Check whether a task number can be inferred.

        Args:
            file_path:
                Document path.

        Returns:
            True if a task identifier is detected.
        """

        return self.detect(file_path) is not None
