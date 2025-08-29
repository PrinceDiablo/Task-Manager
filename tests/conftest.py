# conftest.py
import pytest
from datetime import date, timedelta
from task_manager.task import Task

@pytest.fixture
def sample_task():
    """A simple resuable Task object."""
    return Task(
        title="Sample Task",
        description="description",
        period_start_date=date.today().isoformat(),
        period_end_date=(date.today() + timedelta(days=2)).isoformat(),
        priority=2,
        status="nc"
    )

@pytest.fixture
def overdue_sample_task():
    """A Task that is already overdue."""
    return Task(
        title="Overdue Task",
        period_end_date=(date.today()-timedelta(days=1)).isoformat(),
        priority=1
    )