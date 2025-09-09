"""

Test Configurations.

Shared pytest fixtures for Task tests.
"""

import pytest
from datetime import date, timedelta
from task_manager.task import Task
from task_manager.fileio import FileIO, csv_io, json_io

TODAY = date.today()

@pytest.fixture
def complete_sample_task() -> Task:
    """Task with all fields filled."""
    return Task(
        title="Complete Sample Task",
        period_start_date=TODAY,
        period_end_date=(TODAY + timedelta(days=2)),
        priority=2,
        status="ns",
        description="description"
    )

@pytest.fixture
def sample_task() -> Task:
    """Task using defaults except required fields."""
    return Task(
        title="Sample Task",
        period_end_date=(TODAY + timedelta(days=2))
    )

@pytest.fixture(autouse=True)
def reset_registry():
    """Cleans and Re-registers built-ins."""
    FileIO.exporters.clear()
    FileIO.importers.clear()
    FileIO.register_exporter(".csv", csv_io.export_csv)
    FileIO.register_importer(".csv", csv_io.import_csv)
    FileIO.register_exporter(".json", json_io.export_json)
    FileIO.register_importer(".json", json_io.import_json)