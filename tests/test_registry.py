"""

test File I/O registry.

Unit tests for FileIO: Behavior.
"""

from task_manager.fileio import FileIO, csv_io, json_io
import pytest

# ---- Behavior (correct) ----

def test_register_exporter():
    FileIO.register_exporter(".csv", csv_io.export_csv)
    assert FileIO.exporters[".csv"] is csv_io.export_csv
    FileIO.register_exporter(".csv", json_io.export_json)
    assert FileIO.exporters[".csv"] is json_io.export_json

def test_register_importer():
    FileIO.register_importer(".csv", csv_io.import_csv)
    assert FileIO.importers[".csv"] is csv_io.import_csv
    FileIO.register_importer(".csv", json_io.import_json)
    assert FileIO.importers[".csv"] is json_io.import_json

# ---- Behavior (wrong) ----

def test_no_extension():
    with pytest.raises(ValueError):
        FileIO._extension("")
    with pytest.raises(ValueError):
        FileIO._extension(None)

def test_export_none_date(tmp_path):
    with pytest.raises(ValueError, match="No data to export."):
        FileIO.export(".csv", None, tmp_path)

def test_none_path():
    # None path for exporter
    FileIO.register_exporter("csv", csv_io.export_csv)
    with pytest.raises(ValueError, match="Please provide a valid file path."):
        FileIO.export(".csv", [{"k": "v"}], None)
    # None path for importer
    FileIO.register_importer("csv", csv_io.import_csv)
    with pytest.raises(ValueError, match="Please provide a valid file path."):
        FileIO.import_(".csv", None)

def test_unknown_extension_errors(tmp_path):
    ext = ".yaml"
    # unknown exporter
    with pytest.raises(ValueError, match=f"No exporter registered"):
        FileIO.export(ext, [{"k": "v"}], str(tmp_path / "x.yaml"))
    # unknown importer
    with pytest.raises(ValueError, match=f"No importer registered"):
        FileIO.import_(ext, str(tmp_path / "x.yaml"))