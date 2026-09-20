"""
Archive extraction utilities.
"""

from __future__ import annotations

import logging
import zipfile
from pathlib import Path

import rarfile


LOGGER = logging.getLogger(__name__)


class ArchiveExtractor:
    """
    Extract ZIP and RAR archives recursively.
    """

    SUPPORTED_EXTENSIONS = {
        ".zip",
        ".rar",
    }

    def extract_archive(
        self,
        archive_path: Path,
    ) -> Path:
        """
        Extract a single archive.

        Args:
            archive_path:
                Archive path.

        Returns:
            Extraction directory.
        """

        suffix = archive_path.suffix.lower()

        target_dir = (
            archive_path.parent /
            archive_path.stem
        )

        if target_dir.exists():
            return target_dir

        target_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        if suffix == ".zip":

            with zipfile.ZipFile(
                archive_path,
                "r",
            ) as archive:

                archive.extractall(target_dir)

            return target_dir

        if suffix == ".rar":

            with rarfile.RarFile(
                archive_path
            ) as archive:

                archive.extractall(target_dir)

            return target_dir

        raise ValueError(
            f"Unsupported archive type: {suffix}"
        )

    def extract_recursive(
        self,
        root: Path,
    ) -> list[Path]:
        """
        Recursively extract nested archives until
        no new archives are discovered.

        Args:
            root:
                Root directory.

        Returns:
            List of extraction directories.
        """

        extracted_dirs: list[Path] = []
        processed_archives: set[Path] = set()

        while True:

            archives = [
                path
                for path in root.rglob("*")
                if (
                    path.is_file()
                    and path.suffix.lower()
                    in self.SUPPORTED_EXTENSIONS
                    and path not in processed_archives
                )
            ]

            if not archives:
                break

            LOGGER.info(
                "Found %d archives",
                len(archives),
            )

            for archive in archives:

                try:

                    target = self.extract_archive(
                        archive
                    )

                    extracted_dirs.append(
                        target
                    )

                    processed_archives.add(
                        archive
                    )

                except Exception:

                    LOGGER.exception(
                        "Failed extracting %s",
                        archive,
                    )
        return extracted_dirs
