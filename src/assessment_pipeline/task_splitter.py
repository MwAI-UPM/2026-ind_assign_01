"""
Task section extraction utilities.
"""

from __future__ import annotations

from assessment_pipeline.models import (
    TaskSection,
)

import re


class TaskSplitter:
    """
    Split a monolithic submission into task sections.
    """

    TASK_PATTERNS = {
        1: (
            r"task\s*1\b|"
            r"task\s*one\b"
        ),
        2: (
            r"task\s*2\b|"
            r"task\s*two\b"
        ),
        3: (
            r"task\s*3\b|"
            r"task\s*three\b"
        ),
        4: (
            r"task\s*4\b|"
            r"task\s*four\b"
        ),
        5: (
            r"task\s*5\b|"
            r"task\s*five\b"
        ),
    }

    def split(
        self,
        text: str,
        document_name: str,
    ) -> dict[int, TaskSection]:
        """
        Split a submission into task sections.

        Args:
            text:
                Submission content.

        Returns:
            Mapping of task number to extracted text.
        """

        if not text.strip():
            return {}

        matches: list[tuple[int, int]] = []

        for task_number, pattern in (
            self.TASK_PATTERNS.items()
        ):
            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            )

            if match:
                matches.append(
                    (
                        task_number,
                        match.start(),
                    )
                )

        if not matches:
            return {}

        matches.sort(
            key=lambda item: item[1]
        )

        sections: dict[int, TaskSection] = {}

        for index in range(
            len(matches)
        ):
            task_number = matches[index][0]
            start = matches[index][1]

            if index + 1 < len(matches):
                end = matches[
                    index + 1
                ][1]

            else:
                end = len(text)

            sections[task_number] = TaskSection(
                task_number=task_number,
                text=text[start:end].strip(),
                source_document=document_name,
                characters=len(
                    text[start:end].strip()
                ),
            )

        return sections
