"""
Submission serialization utilities.
"""

from __future__ import annotations

import json
from pathlib import Path

from assessment_pipeline.models import (
    ExtractedDocument,
    StudentSubmission,
)


class JsonNormalizer:
    """
    Serialize student submissions into JSON files.
    """

    def serialize_document(
        self,
        document: ExtractedDocument,
    ) -> dict:
        """
        Convert a document into a JSON-serializable structure.

        Args:
            document:
                Extracted document.

        Returns:
            Dictionary representation.
        """

        return {
            "file_name": document.file_name,
            "extension": document.extension,
            "source_path": document.source_path,
            "size_bytes": document.size_bytes,
            "characters": document.characters,
            "task_number": document.task_number,
            "text_content": document.text_content,
        }

    def serialize_submission(
        self,
        submission: StudentSubmission,
    ) -> dict:
        """
        Convert a student submission into a JSON-serializable
        structure.

        Args:
            submission:
                Student submission.

        Returns:
            Dictionary representation.
        """

        return {
            "student_name": submission.student_name,
            "student_id": submission.student_id,
            "source_folder": submission.source_folder,
            "total_documents": submission.total_documents,
            "total_characters": submission.total_characters,
            "documents": [
                self.serialize_document(document)
                for document in submission.documents
            ],
            "task_summary": {
                str(document.task_number): {
                    "file_name": document.file_name,
                    "characters": document.characters,
                    "extension": document.extension,
                }
                for document in submission.documents
                if document.task_number is not None
            },
            "documents": [
                self.serialize_document(document)
                for document in submission.documents
            ],
        }

    def write(
        self,
        submission: StudentSubmission,
        output_path: Path,
    ) -> None:
        """
        Write a normalized submission to disk.

        Args:
            submission:
                Student submission.

            output_path:
                Target JSON file.
        """

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = self.serialize_submission(
            submission
        )

        with output_path.open(
            mode="w",
            encoding="utf-8",
        ) as file_handle:

            json.dump(
                payload,
                file_handle,
                indent=4,
                ensure_ascii=False,
            )
