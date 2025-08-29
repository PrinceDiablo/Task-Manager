from fileio import FileIO
import csv

def export_csv(data: list[dict], path: str) -> str:
    """Export List as .csv file"""
    try:
        with open(path, "w") as file:
            writer = csv.DictWriter(file, fieldnames = data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return f"Expoted Successfully "
    except FileNotFoundError:
        raise FileNotFoundError("No such path or file exists.")
def import_csv(path: str) -> any:
    """Import List as .csv file"""
    try:
        with open(path,"r") as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        raise FileNotFoundError("No such path or file exists.")

FileIO.register_exporter("csv", export_csv)
FileIO.register_importer("csv", import_csv)