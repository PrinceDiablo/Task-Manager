from . import FileIO
import csv

def export_csv(data: list[dict], path: str) -> str:
    """Export List as .csv file"""
    with open(path, "w") as file:
        writer = csv.DictWriter(file, fieldnames = data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    return f"\nExpoted Successfully "

def import_csv(path: str) -> any:
    """Import List as .csv file"""
    with open(path,"r") as file:
        reader = csv.DictReader(file)
        return list(reader)

FileIO.register_exporter(".csv", export_csv)
FileIO.register_importer(".csv", import_csv)