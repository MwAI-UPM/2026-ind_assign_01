"""
Text document parsing utilities.
"""

from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup


class TextParser:
    """
    Extract textual content from text-based files.

    Supported formats:

    - TXT
    - MD
    - CSV
    - HTML

    The parser automatically selects the optimal
    extraction strategy based on the file extension.
    """

    SUPPORTED_EXTENSIONS = {
        ".txt",
        ".md",
        ".csv",
        ".html",
    }

    def extract_text(
        self,
        file_path: Path,
    ) -> str:
        """
        Extract textual content from a supported file.

        Args:
            file_path:
                Path to the source file.

        Returns:
            Extracted textual content.

        Raises:
            ValueError:
                If the file extension is unsupported.
        """

        extension = file_path.suffix.lower()

        if extension in {".txt", ".md"}:
            return self._extract_plain_text(file_path)

        if extension == ".csv":
            return self._extract_csv(file_path)

        if extension == ".html":
            return self._extract_html(file_path)

        raise ValueError(
            f"Unsupported text format: {extension}"
        )

    def _extract_plain_text(
        self,
        file_path: Path,
    ) -> str:
        """
        Read a plain text file.

        Args:
            file_path:
                Source file.

        Returns:
            File content.
        """

        return file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    def _extract_csv(
        self,
        file_path: Path,
    ) -> str:
        """
        Read a CSV file as plain text.

        Args:
            file_path:
                Source CSV file.

        Returns:
            CSV textual representation.
        """

        return file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    def _extract_html(
        self,
        file_path: Path,
    ) -> str:
        """
        Extract visible text from an HTML document.

        Args:
            file_path:
                Source HTML file.

        Returns:
            Visible textual content.
        """

        html_content = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        soup = BeautifulSoup(
            html_content,
            "html.parser",
        )

        return soup.get_text(
            separator="\n",
            strip=True,
        )
