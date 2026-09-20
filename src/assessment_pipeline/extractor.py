"""
Submission extraction services.
"""

from __future__ import annotations

from pathlib import Path

from assessment_pipeline.models import (
    ExtractedDocument,
    StudentSubmission,
)
from assessment_pipeline.parser_registry import (
    ParserRegistry,
)
from assessment_pipeline.task_detector import (
    TaskDetector,
)
from assessment_pipeline.utils.archive import (
    ArchiveExtractor,
)
from assessment_pipeline.utils.discovery import (
    FileDiscovery,
)
from assessment_pipeline.task_splitter import (
    TaskSplitter,
)


class SubmissionExtractor:
    """
    Extract and normalize a Moodle submission.

    This service coordinates archive extraction,
    document discovery and document parsing.
    """

    def __init__(self) -> None:
        """
        Initialize extractor dependencies.
        """

        self._archive_extractor = (
            ArchiveExtractor()
        )

        self._file_discovery = (
            FileDiscovery()
        )

        self._parser_registry = (
            ParserRegistry()
        )

        self._task_detector = (
            TaskDetector()
        )

    def extract(
        self,
        student_name: str,
        student_id: str,
        submission_folder: Path,
    ) -> StudentSubmission:
        """
        Process a Moodle submission folder.

        Args:
            student_name:
                Student full name.

            student_id:
                Moodle identifier.

            submission_folder:
                Moodle submission directory.

        Returns:
            Canonical student submission.
        """

        self._archive_extractor.extract_recursive(
            submission_folder
        )

        files = self._file_discovery.discover(
            submission_folder
        )

        submission = StudentSubmission(
            student_name=student_name,
            student_id=student_id,
            source_folder=str(submission_folder),
        )

        splitter = TaskSplitter()

        for file_path in files:

            parser = (
                self._parser_registry.get_parser(
                    file_path.suffix
                )
            )

            if parser is None:
                continue

            try:

                text = parser.extract_text(
                    file_path
                )

            except Exception as exc:

                print(
                    f"Failed parsing "
                    f"{file_path}: {exc}"
                )

                continue

            document = ExtractedDocument(
                file_name=file_path.name,
                extension=file_path.suffix.lower(),
                source_path=str(file_path),
                size_bytes=file_path.stat().st_size,
                characters=len(text),
                task_number=(
                    self._task_detector.detect(
                        file_path
                    )
                ),
                text_content=text,
            )

            submission.documents.append(
                document
            )

            if (
                document.task_number is None
                and document.text_content
                and len(document.text_content) > 10000
            ):
                sections = splitter.split(
                    text=document.text_content,
                    document_name=document.file_name,
                )

                submission.task_sections.extend(
                    sections.values()
                )

        return submission
