class FileIO:
    """Imports and Exports Task lists to files."""
    exporters = {}
    importers = {}

    @classmethod
    def register_exporter(cls, name: str, function) -> None:
        """Add extension name and its defined function"""
        cls.exporters[name] = function
    
    @classmethod
    def register_importer(cls, name: str, function) -> None:
        """Add extension name and its defined function"""
        cls.importers[name] = function

    @classmethod
    def export(cls, format_name: str, data: list[dict], path: str) -> str:
        """Export to file"""
        exporter = cls.exporters.get(format_name)
        if not exporter:
            raise ValueError(f"\nFormat '{format_name}' is not supported.")
        return exporter(data, path)

    @classmethod
    def import_(cls, format_name: str, path: str) -> list:
        """Import from file"""
        importer = cls.importers.get(format_name)
        if not importer:
            raise ValueError(f"\nFormat '{format_name}' is not supported.")
        return importer(path)