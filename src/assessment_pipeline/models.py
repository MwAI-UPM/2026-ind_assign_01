"""
Domain models used by the assessment pipeline.
"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(slots=True)
class ExtractedDocument:
    """
    Represents a document extracted from a student submission.

    Attributes:
        file_name:
            Original file name.

        extension:
            File extension including the leading dot.

        source_path:
            Absolute path of the source file.

        size_bytes:
            File size expressed in bytes.

        characters:
            Number of extracted text characters.

        task_number:
            Assignment task inferred from the file name.
            None if no task can be inferred.

        text_content:
            Text extracted from the document.
    """

    file_name: str
    extension: str
    source_path: str
    size_bytes: int
    characters: int
    task_number: int | None
    text_content: str


@dataclass(slots=True)
class TaskSection:
    """
    A logical task extracted from a submission.
    """

    task_number: int

    text: str

    source_document: str

    characters: int


@dataclass(slots=True)
class StudentSubmission:
    """
    Canonical representation of a Moodle submission.

    Attributes:
        student_name:
            Full name inferred from Moodle export.

        student_id:
            Moodle internal identifier.

        source_folder:
            Original Moodle submission folder.

        documents:
            Collection of extracted documents.
    """

    student_name: str
    student_id: str
    source_folder: str
    task_sections: list[TaskSection] = field(
        default_factory=list
    )
    documents: list[ExtractedDocument] = field(
        default_factory=list
    )

    @property
    def total_characters(self) -> int:
        """
        Compute the total amount of extracted text.

        Returns:
            Total number of extracted characters.
        """
        return sum(
            document.characters
            for document in self.documents
        )

    @property
    def total_documents(self) -> int:
        """
        Compute the total number of documents.

        Returns:
            Number of parsed documents.
        """
        return len(self.documents)

    @property
    def full_submission_text(
        self,
    ) -> str:
        """
        Aggregate all document text.
    
        Returns:
            Complete submission text.
        """
    
        chunks = []

        for document in self.documents:

            chunks.append(
                f"===== {document.file_name} ====="
            )

            chunks.append(
                document.text_content
            )

        return "\n\n".join(chunks)

    @property
    def task_documents(
        self,
    ) -> list[ExtractedDocument]:
        """
        Return documents associated with tasks.

        Returns:
            Documents with detected task number.
        """

        return [
            document
            for document in self.documents
            if document.task_number is not None
        ]

    @property
    def auxiliary_documents(
        self,
    ) -> list[ExtractedDocument]:
        """
        Return non-task documents.

        Returns:
            Auxiliary supporting documents.
        """

        return [
            document
            for document in self.documents
            if document.task_number is None
        ]

    @property
    def section_coverage(self) -> float:
        """Return the fraction of extracted text assigned to task sections.

        Returns:
            A value between 0.0 and 1.0.  Returns 0.0 when the submission has
            no extracted text.
        """

        if self.total_characters == 0:
            return 0.0

        section_characters = sum(
            section.characters
            for section in self.task_sections
        )

        return (
            section_characters
            / self.total_characters
        )

