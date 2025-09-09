"""

Test JSON handler.

Unit tests for FileIO: json section.
"""
import pytest
import json
from task_manager.fileio import FileIO, json_io
from task_manager import Task

def test_export_json_none_data(tmp_path):
    path = tmp_path / "tasks.json"
    with pytest.raises(ValueError, match="No data to export"):
        json_io.export_json(None, str(path))

def test_json_round_trip(tmp_path, sample_task: Task):
    path = tmp_path / "tasks.json"
    data = [sample_task.to_dict()]
    massage = FileIO.export(".json", data, str(path))
    assert "Exported" in massage
    loaded = FileIO.import_(".json", str(path))
    assert loaded == data

def test_json_export_none_data_raises(tmp_path):
    path = tmp_path / "tasks.json"
    with pytest.raises(ValueError, match="No data to export"):
        FileIO.export(".json", None, str(path))

def test_json_import_bad_json_raises(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{bad json", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        FileIO.import_(".json", str(path))