# test_task.py
import pytest
from datetime import date, timedelta
from task_manager.task import Task

def test_task_fixture(sample_task):
    assert sample_task.title == "Sample Task"
    assert sample_task.priority == 2
    assert sample_task.status in ("nc", "not started")

def test_overdue_fixture(overdue_sample_task):
    assert overdue_sample_task.is_overdue() is True

def test_update_status(sample_task):
    sample_task.mark_in_progress()
    assert sample_task.status in ("inp", "in-progress") 