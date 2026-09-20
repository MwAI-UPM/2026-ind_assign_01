"""
Document discovery utilities.
"""

from __future__ import annotations

from pathlib import Path


class FileDiscovery:
    """
    Discover supported files recursively.
    """

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".pptx",
        ".xlsx",
        ".txt",
        ".csv",
        ".html",
        ".md",
    }

    def discover(
        self,
        root: Path,
    ) -> list[Path]:
        """
        Discover supported documents.

        Args:
            root:
                Search root directory.

        Returns:
            Sorted list of files.
        """

        discovered: list[Path] = []

        for candidate in root.rglob("*"):

            if not candidate.is_file():
                continue

            if (
                candidate.suffix.lower()
                not in self.SUPPORTED_EXTENSIONS
            ):
                continue

            if self._should_ignore(candidate):
                continue

            discovered.append(candidate)
        return sorted(discovered)

    def _should_ignore(
        self,
        path: Path,
    ) -> bool:
        """
        Determine whether a file should be ignored.

        Args:
            path:
                Candidate path.

        Returns:
            True if ignored.
        """

        return (
            "__MACOSX" in path.parts
            or path.name.startswith("._")
            or path.name.startswith("~$")
            or path.name == ".DS_Store"
        )
