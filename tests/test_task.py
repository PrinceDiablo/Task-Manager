"""

Test Task.

Unit tests for Task: validation, behavior, serialization, formatting.
"""
import pytest
from datetime import date, timedelta
from task_manager.task import Task

TODAY = date.today()

# ---- Fixtures sanity check ----

def test_task_fixture_value(complete_sample_task: Task):
    assert complete_sample_task.title == "Complete Sample Task"
    assert complete_sample_task.period_start_date == TODAY
    assert complete_sample_task.period_end_date == TODAY + timedelta(days=2)
    assert complete_sample_task.priority == 2
    assert complete_sample_task.status == "ns"
    assert complete_sample_task.description == "description"

# ---- Defaults ----

def test_default_values(sample_task: Task):
    assert sample_task.title =="Sample Task"
    assert sample_task.period_start_date == TODAY
    assert sample_task.period_end_date ==(TODAY + timedelta(days=2))
    assert sample_task.priority == 3
    assert sample_task.status == "ns"

# ---- Status change methods ----

def test_marked_complete_sets_status_c(complete_sample_task: Task):
    complete_sample_task.marked_complete()
    assert complete_sample_task.status == "c"

def test_marked_not_started_sets_status_ns(complete_sample_task: Task):
    complete_sample_task.marked_not_started()
    assert complete_sample_task.status == "ns" 

def test_mark_in_progress_sets_status_inp(complete_sample_task: Task):
    complete_sample_task.mark_in_progress()
    assert complete_sample_task.status == "inp"

# ---- Overdue logic ----

def test_is_overdue_when_end_date_in_past():
    t = Task(title="Test", period_start_date = (TODAY - timedelta(days=2)), period_end_date=(TODAY - timedelta(days=1)))
    assert t.is_overdue() is True

def test_is_not_overdue_when_end_date_is_today():
    t = Task(title="Test", period_end_date=TODAY) 
    assert t.is_overdue() is False     

# ---- Serialization ----

def test_to_dict_matches_expected_schema(sample_task: Task):
    dictionary = {
        "title": "Sample Task",
        "period_start_date": TODAY.isoformat(),
        "period_end_date": (TODAY + timedelta(days=2)).isoformat(),
        "priority": 3,
        "status": "ns",
        "description": ""
    } 
    assert sample_task.to_dict() == dictionary

def test_from_dict_builds_equivalent_task(complete_sample_task: Task):
    
    dictionary = {
        "title": "Complete Sample Task",
        "period_start_date": TODAY.isoformat(),
        "period_end_date": (TODAY + timedelta(days=2)).isoformat(),
        "priority": 2,
        "status": "ns",
        "description": "description"  
    }
    assert Task.from_dict(dictionary) == complete_sample_task

def test_to_dict_then_from_dict_preserves_fields(sample_task: Task):
    dictionary = sample_task.to_dict()
    t2 = Task.from_dict(dictionary)
    assert sample_task.title == t2.title
    assert sample_task.period_start_date == t2.period_start_date
    assert sample_task.period_end_date == t2.period_end_date
    assert sample_task.priority == t2.priority
    assert sample_task.status == t2.status
    assert sample_task.description == t2.description

def test_roundtrip_to_from_to_dict_is_stable(sample_task: Task):
    dictionary = sample_task.to_dict()
    t = Task.from_dict(dictionary)
    dictionary2 = t.to_dict()
    assert dictionary2 == {
        "title": "Sample Task",
        "period_start_date": TODAY.isoformat(),
        "period_end_date": (TODAY + timedelta(days=2)).isoformat(),
        "priority": 3,
        "status": "ns",
        "description": ""
    }     

# ---- Representation ----

def test_repr_includes_all_core_fields(sample_task: Task):
    r = repr(sample_task)
    assert "Task(" in r
    assert f"title='{str(sample_task.title)}'" in r
    assert f"period_start_date={str(sample_task.period_start_date)}" in r
    assert f"period_end_date={str(sample_task.period_end_date)}" in r
    assert f"priority={str(sample_task.priority)}" in r
    assert f"status='{str(sample_task.status)}'" in r
    assert f"description='{str(sample_task.description)}'" in r

def test_str_includes_title_dates_priority_status_description_placeholder(sample_task: Task):
    s = str(sample_task)
    assert "Sample Task" in s
    assert str(sample_task.period_start_date) in s
    assert str(sample_task.period_end_date) in s
    assert "Medium" in s
    assert "Not Started" in s
    assert "(No Description)" in s

# ---- Validation (title)----

def test_str_contains_title():
    t = Task(title="Test", period_end_date=TODAY)
    assert "Test" in str(t)

def test_blank_title_raises():
    with pytest.raises(ValueError):
        Task(title="", period_end_date=TODAY)

# ---- Validation (date)----

def test_valid_date_parsing_and_order():
    # Same end and start date check, string to date obj check
    t = Task(title="Test", period_start_date=TODAY, period_end_date=TODAY.isoformat())
    assert t.period_end_date == TODAY
    # End date is greater than start date check
    t = Task(title="Test", period_start_date=TODAY, period_end_date=(TODAY + timedelta(days=2)))
    assert t.period_end_date == (TODAY + timedelta(days=2))
    # Leap year check
    t = Task(title="Test", period_end_date="2028-02-29")
    assert t.period_end_date == date(2028, 2, 29)

def test_start_setter_does_not_access_missing_end():
    # Bypass __init__ to simulate "end not set yet"
    t = Task.__new__(Task)
    t.title = "Test"
    # Should not raise AttributeError
    t.period_start_date = date.today()

def test_end_setter_does_not_access_missing_start():
    # Bypass __init__ to simulate "start not set yet"
    t = Task.__new__(Task)
    t.title = "Test"
    # Should not raise AttributeError
    t.period_end_date = date.today()

def test_setting_start_date_after_existing_end_raises_value_error():
    # End set first, then try to push start after end -> should raise
    t = Task(title="Test", period_end_date=TODAY + timedelta(days=2))
    with pytest.raises(ValueError):
        t.period_start_date = TODAY + timedelta(days=3)

def test_setting_end_before_existing_start_raises():
    # Start set first, then try to set end before start -> should raise
    t = Task(title="Test", period_start_date=date.today(), period_end_date=date.today() + timedelta(days=2))
    with pytest.raises(ValueError):
        t.period_end_date = date.today() - timedelta(days=1)

@pytest.mark.parametrize("raw",["not-a-date", "02-05-2024", "2024/05/02"])
def test_invalid_date_format_raises(raw):
    with pytest.raises(ValueError):
        Task(title="Test", period_end_date=raw)

def test_end_date_before_start_date_raises():
    with pytest.raises(ValueError):
        Task(title="Test",period_start_date=TODAY,period_end_date=TODAY- timedelta(days=2))

@pytest.mark.parametrize("pri", [6, -1, 0, "One"])
def test_invalid_priority_raises(pri):
    with pytest.raises(ValueError):
        Task(title="Test", period_end_date=TODAY, priority=pri)

def test_invalid_status_raises():
    with pytest.raises(ValueError):
        Task(title="Test", period_end_date=TODAY, status="done")

# ---- Validation (other) ----


def test_valid_priority_string_inputs():
    t = Task(title="Test", period_end_date=TODAY, priority="5") # Max
    assert t.priority == 5
    t = Task(title="Test", period_end_date=TODAY, priority="1") # Min
    assert t.priority == 1

def test_valid_status_normalization():
    t = Task(title="Test", period_end_date=TODAY, status="ComPleted")
    assert t.status == "c"
    t = Task(title="Test", period_end_date=TODAY, status="not started")
    assert t.status == "ns"
    t = Task(title="Test", period_end_date=TODAY, status="in-progress")
    assert t.status == "inp"
    t = Task(title="Test", period_end_date=TODAY, status="INP") # Case incensitive
    assert t.status == "inp" 

def test_description_none_normalized():
    t = Task(title="Test", period_end_date=date.today(), description=None)
    assert t.description == ""

# ---- Validation (Test.eq) ----

def test_inequality_with_different_title(sample_task: Task):
    other = Task(title="Different", period_end_date=sample_task.period_end_date)
    assert sample_task != other
    
def test_eq_special_method_results_notimplemented(sample_task: Task):
    assert Task.__eq__(sample_task, 123) is NotImplemented
    assert Task.__eq__(sample_task, object()) is NotImplemented

def test_eq_operator_with_non_task_is_false(sample_task: Task):
    assert (sample_task == 123) is False
    assert (123 == sample_task) is False
