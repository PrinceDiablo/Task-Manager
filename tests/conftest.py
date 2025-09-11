"""

Test Configurations.

Shared pytest fixtures for Task tests.
"""

import pytest
from datetime import date, timedelta
from task_manager import Task, TaskManager
from task_manager.fileio import FileIO, csv_io, json_io

TODAY: date = date.today()

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

@pytest.fixture
def overdue_task() -> Task:
    """Task that is overdue"""
    return Task(
        title="overdue_1", 
        period_start_date=(TODAY - timedelta(days=2)), 
        period_end_date=(TODAY - timedelta(days=1))
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

@pytest.fixture
def task_list(sample_task: Task, complete_sample_task: Task, overdue_task: Task) -> list[dict]: 
    task_overdue = Task(title="overdue_2", period_start_date=(TODAY - timedelta(days=4)), period_end_date=(TODAY - timedelta(days=2)))
    task_highest_priority = Task(title="Test", period_start_date=(TODAY - timedelta(days=2)), period_end_date=(TODAY + timedelta(days=1)), priority=1)
    m1 = TaskManager()
    m1.add_task(sample_task)
    m1.add_task (complete_sample_task)
    m1.add_task(overdue_task)
    m1.add_task(task_overdue)
    m1.add_task(task_highest_priority)
    return m1.to_dict_list()