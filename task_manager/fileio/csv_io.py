"""

CSV handlers.

Export/import a list of dicts to/from CSV. 
Registers CSV handlers with FileIO on import.
"""

import csv
from . import FileIO

def export_csv(data: list[dict], path: str) -> str:
    """Write list of dicts to CSV."""
    # CSV needs at least one row to infer headers.
    if not data:
        raise ValueError("No data to export.")
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames = data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    return "Exported Successfully."

def import_csv(path: str) -> list[dict]:
    """Read list of dicts from CSV."""
    with open(path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)

FileIO.register_exporter(".csv", export_csv)
FileIO.register_importer(".csv", import_csv)