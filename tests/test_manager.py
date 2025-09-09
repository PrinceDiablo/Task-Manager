"""

Test Task manager core.

Unit tests for TaskManager: validation, behavior.
"""

from task_manager import TaskManager
from task_manager.task import Task
import pytest
from datetime import date, timedelta

# ---- Success ----

def test_add_task(complete_sample_task: Task, sample_task: Task):
    m1 = TaskManager()
    result = m1.add_task(complete_sample_task)
    result2 = m1.add_task(sample_task)
    assert complete_sample_task in m1.tasks
    assert sample_task in m1.tasks
    assert f"Task '{complete_sample_task.title}' has been added successfully." == result
    assert f"Task '{sample_task.title}' has been added successfully." == result2

def test_delete_task(complete_sample_task: Task, sample_task: Task):
    m1 = TaskManager()
    m1.add_task(complete_sample_task)
    m1.add_task(sample_task)
    result = m1.delete_task(2)
    result2 = m1.delete_task(1)
    assert f"Task '{sample_task.title}' has been deleted successfully." == result
    assert f"Task '{complete_sample_task.title}' has been deleted successfully." == result2

def test_index_after_delete(sample_task: Task, complete_sample_task: Task):
    m = TaskManager()
    m.add_task(sample_task)
    m.add_task(complete_sample_task)
    m.delete_task(1)
    rows = list(m.view_tasks())
    assert rows[0].startswith("1.")
    assert "Complete Sample Task" in rows[0]

def test_delete_last_task(sample_task: Task):
    m1 = TaskManager()
    m1.add_task(sample_task)
    m1.delete_task(1)
    assert m1.tasks == []

def test_update_task(complete_sample_task: Task, sample_task: Task):
    m1 = TaskManager()
    m1.add_task(complete_sample_task)
    m1.add_task(sample_task)
    result = m1.update_task(1, sample_task)
    result2 = m1.update_task(2, complete_sample_task)
    assert f"Task '{sample_task.title}' updated successfully." == result
    assert f"Task '{complete_sample_task.title}' updated successfully." == result2
    # Check only target update
    m1.update_task(1, complete_sample_task)
    assert m1.tasks[0] == complete_sample_task
    assert m1.tasks[1] == complete_sample_task

def test_duplicate_tasks_allowed(sample_task: Task):
    m1 = TaskManager()
    m1.add_task(sample_task)
    m1.add_task(sample_task)
    assert len(m1.tasks) == 2 


def test_update_status(sample_task: Task):
    m1 = TaskManager()
    m1.add_task(sample_task)
    assert m1.tasks[0].status == 'ns'
    sample_task.mark_in_progress()
    m1.update_task(1, sample_task)
    assert m1.tasks[0].status == 'inp' 
    sample_task.marked_complete()
    m1.update_task(1, sample_task)
    assert m1.tasks[0].status == 'c'

def test_view_tasks(sample_task: Task):
    m1 = TaskManager()
    m1.add_task(sample_task)
    rows = list(m1.view_tasks())
    assert len(rows) == 1
    assert rows[0].startswith("1.")
    assert "Sample Task" in rows[0]

def test_to_dict_list(sample_task: Task, complete_sample_task: Task):
    m1 = TaskManager()
    today = date.today()
    m1.add_task(sample_task)
    m1.add_task(complete_sample_task)
    data = m1.to_dict_list() 
    assert data == [
        {
            "title":"Sample Task",
            "period_start_date":today.isoformat(),
            "period_end_date":(today + timedelta(days=2)).isoformat(),
            "priority":3,
            "status":"ns",
            "description":""
        },
        {
            "title":"Complete Sample Task",
            "period_start_date": today.isoformat(),
            "period_end_date":(today + timedelta(days=2)).isoformat(),
            "priority":2,
            "status":"ns",
            "description":"description"
        }
    ] 

def test_empty_tasklist_to_dict_list():
    m1 = TaskManager()
    data = m1.to_dict_list()
    assert data == []

# ---- Error ----

def test_add_task_none():
    m1 = TaskManager()
    with pytest.raises(ValueError):
        m1.add_task(None)

def test_invalid_index(sample_task: Task, complete_sample_task: Task):
    m1 = TaskManager()
    with pytest.raises(ValueError): # delete on empty list
        m1.delete_task(1)
    m1.add_task(sample_task)
    m1.add_task(complete_sample_task)
    with pytest.raises(ValueError): # below range (0)
        m1.update_task(0, sample_task)
    with pytest.raises(ValueError):
        m1.delete_task(0)    
    with pytest.raises(ValueError): # above range
        m1.update_task(len(m1.tasks) + 1, sample_task)
    with pytest.raises(ValueError):
        m1.delete_task(len(m1.tasks) + 1)    
    with pytest.raises(ValueError): # non-numeric
        m1.update_task("one", complete_sample_task)
    with pytest.raises(ValueError):
        m1.delete_task("two")
    with pytest.raises(ValueError): # task is None
        m1.update_task(1, None)

def test_empty_tasklist_view():
    m1 = TaskManager()
    with pytest.raises(ValueError):
        list(m1.view_tasks())
    
