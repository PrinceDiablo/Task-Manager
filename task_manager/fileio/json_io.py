"""

JSON handlers.

Export/import a list of dicts to/from JSON. 
Registers JSON handlers with FileIO on import.
"""

import json
from . import FileIO

def export_json(data: list[dict], path: str) -> str:
    """Write list of dicts to JSON."""
    if data is None:
        raise ValueError("No data to export.")
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file,ensure_ascii=False, indent=2)
    return "Exported Successfully."

def import_json(path: str) -> list[dict]:
    """Read list of dicts from JSON."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


FileIO.register_exporter(".json", export_json)
FileIO.register_importer(".json", import_json)