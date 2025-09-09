"""

Test CSV handler.

Unit tests for FileIO: csv section.
"""
import pytest
from task_manager.fileio import FileIO, csv_io
from task_manager import Task


def test_csv_round_trip(tmp_path, sample_task: Task):
    path = tmp_path / "tasks.csv"
    data = [sample_task.to_dict()]
    massage = FileIO.export(".csv", data, str(path))
    assert "Exported" in massage
    loaded = FileIO.import_(".csv", str(path))
    assert loaded[0]["title"] == data[0]["title"]

def test_csv_empty_data_export_raises(tmp_path):
    path = tmp_path / "empty.csv"
    with pytest.raises(ValueError, match="No data to export."):
        FileIO.export(".csv", [], str(path))