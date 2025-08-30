from . import FileIO
import json

def export_json(data: list[dict], path: str) -> str:
    """Export List as .json file"""
    with open(path, "w") as file:
        json.dump(data, file, indent=2)
    return f"\nExpoted Successfully "

def import_json(path: str) -> any:
    """Import List as .json file"""
    with open(path, "r") as file:
        return json.load(file)


FileIO.register_exporter(".json", export_json)
FileIO.register_importer(".json", import_json)