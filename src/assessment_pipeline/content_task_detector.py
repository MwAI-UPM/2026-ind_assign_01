"""
Task detection from document content.
"""

from __future__ import annotations

import re


class ContentTaskDetector:
    """
    Detect assignment tasks inside document text.
    """

    TASK_PATTERNS = {
        1: re.compile(
            r"\btask\s*1\b",
            flags=re.IGNORECASE,
        ),
        2: re.compile(
            r"\btask\s*2\b",
            flags=re.IGNORECASE,
        ),
        3: re.compile(
            r"\btask\s*3\b",
            flags=re.IGNORECASE,
        ),
        4: re.compile(
            r"\btask\s*4\b",
            flags=re.IGNORECASE,
        ),
        5: re.compile(
            r"\btask\s*5\b",
            flags=re.IGNORECASE,
        ),
    }

    def detect_tasks(
        self,
        text: str,
    ) -> set[int]:
        """
        Detect tasks mentioned in a document.

        Args:
            text:
                Document content.

        Returns:
            Set of detected task numbers.
        """

        detected: set[int] = set()

        for task_number, pattern in (
            self.TASK_PATTERNS.items()
        ):

            if pattern.search(text):

                detected.add(task_number)

        return detected
