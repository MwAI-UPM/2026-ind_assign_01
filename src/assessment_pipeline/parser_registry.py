"""
Parser registry.

This module provides a centralized mechanism for
resolving document parsers based on file extensions.
"""

from __future__ import annotations

from assessment_pipeline.parsers.docx_parser import (
    DocxParser,
)
from assessment_pipeline.parsers.pdf_parser import (
    PdfParser,
)
from assessment_pipeline.parsers.pptx_parser import (
    PptxParser,
)
from assessment_pipeline.parsers.text_parser import (
    TextParser,
)
from assessment_pipeline.parsers.xlsx_parser import (
    XlsxParser,
)


class ParserRegistry:
    """
    Resolve parsers from file extensions.

    The registry exposes a single parser instance
    per supported file type.
    """

    def __init__(self) -> None:
        """
        Initialize parser registry.
        """

        text_parser = TextParser()

        self._registry = {
            ".pdf": PdfParser(),
            ".docx": DocxParser(),
            ".pptx": PptxParser(),
            ".xlsx": XlsxParser(),
            ".txt": text_parser,
            ".csv": text_parser,
            ".md": text_parser,
            ".html": text_parser,
        }

    def get_parser(
        self,
        extension: str,
    ):
        """
        Return parser associated with a file extension.

        Args:
            extension:
                File extension.

        Returns:
            Parser instance or None if unsupported.
        """

        return self._registry.get(
            extension.lower()
        )

    def is_supported(
        self,
        extension: str,
    ) -> bool:
        """
        Check whether an extension is supported.

        Args:
            extension:
                File extension.

        Returns:
            True if supported.
        """

        return (
            extension.lower()
            in self._registry
        )

    @property
    def supported_extensions(
        self,
    ) -> set[str]:
        """
        Return supported extensions.

        Returns:
            Set of supported extensions.
        """

        return set(
            self._registry.keys()
        )
