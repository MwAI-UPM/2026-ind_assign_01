"""
PDF parsing utilities.
"""

from __future__ import annotations

import logging
from pathlib import Path

from pypdf import PdfReader


LOGGER = logging.getLogger(__name__)


class PdfParser:
    """
    Extract textual content from PDF documents.
    """

    def extract_text(
        self,
        pdf_path: Path,
    ) -> str:
        """
        Extract textual content from a PDF document.

        Args:
            pdf_path:
                Path to the PDF file.

        Returns:
            Concatenated textual content from all pages.
        """

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF not found: {pdf_path}"
            )

        reader = PdfReader(str(pdf_path))

        pages_text: list[str] = []

        empty_pages = 0

        total_pages = len(reader.pages)

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):

            try:

                text = page.extract_text()

                if text and text.strip():

                    pages_text.append(text)

                else:

                    empty_pages += 1

            except Exception as exc:

                LOGGER.warning(
                    (
                        "Failed extracting page %d "
                        "from %s: %s"
                    ),
                    page_number,
                    pdf_path.name,
                    exc,
                )

        if (
            total_pages > 0
            and empty_pages == total_pages
        ):

            LOGGER.warning(
                (
                    "PDF appears to contain "
                    "no extractable text: %s"
                ),
                pdf_path,
            )

        return "\n\n".join(pages_text)

    def get_page_count(
        self,
        pdf_path: Path,
    ) -> int:
        """
        Retrieve the number of pages in a PDF document.

        Args:
            pdf_path:
                Path to the PDF file.

        Returns:
            Number of pages.
        """

        reader = PdfReader(str(pdf_path))

        return len(reader.pages)
