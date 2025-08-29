from fileio import FileIO
import json

def export_json(data: list[dict], path: str) -> str:
    """Export List as .json file"""
    try:
        with open(path, "w") as file:
            json.dump(data, file, indent=2)
        return f"Expoted Successfully "
    except FileNotFoundError:
        raise FileNotFoundError("No such path or file exists.")

def import_json(path: str) -> any:
    """Import List as .json file"""
    try:
        with open(path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("No such path or file exists.")


FileIO.register_exporter("json", export_json)
FileIO.register_importer("json", import_json)