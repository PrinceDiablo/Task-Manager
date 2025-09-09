"""

File I/O registry.

Registers exporters/importers by file extension (e.g., ".csv", ".json") and
dispatches export/import calls to the right handler.
"""

from typing import Callable
from os import PathLike

Exporter = Callable[[list[dict], str], str]
Importer = Callable[[str], list[dict]]

class FileIO:
    """Imports and Exports Task lists to files."""
    exporters: dict[str, Exporter] = {}
    importers: dict[str, Importer] = {}

    @staticmethod
    def _extension(ext: str) -> str:
        if not ext:
            raise ValueError("File extension is required.")
        ext = ext.strip().lower()
        return ext if ext.startswith(".") else f".{ext}"

    @classmethod
    def register_exporter(cls, ext: str, func: Exporter) -> None:
        """Register an exporter for the given extension."""
        cls.exporters[cls._extension(ext)] = func
    
    @classmethod
    def register_importer(cls, ext: str, func: Callable) -> None:
        """Register an importer for the given extension."""
        cls.importers[cls._extension(ext)] = func

    @classmethod
    def export(cls, ext: str, data: list[dict], path: str | PathLike[str]) -> str:
        """Export data using the registered exporter for ext."""
        if not path:
            raise ValueError("Please provide a valid file path.")
        if data is None:
            raise ValueError("No data to export.")
        extension = cls._extension(ext)
        if extension not in cls.exporters:
            raise ValueError(f"No exporter registered for {extension}.")
        return cls.exporters[extension](data, str(path))

    @classmethod
    def import_(cls, ext: str, path: str | PathLike[str]) -> list[dict]:
        """Import data using the registered importer for ext."""
        if not path:
            raise ValueError("Please provide a valid file path.")
        extension = cls._extension(ext)
        if extension not in cls.importers:
            raise ValueError(f"No importer registered for {extension}.")
        return cls.importers[extension](str(path))
    