"""

Test Report module.

Unit test for Reports: empty input, no-result, sorting, column shaping.
"""

import pytest
from task_manager import reports, TaskManager, Task


def test_get_overdue_reports(task_list: list[dict]):
    df = reports.get_overdue_report(task_list)
    assert  not df.empty
    assert len(df) == 2
    assert df.iloc[0]["title"] == "overdue_2"
    assert df.iloc[0]["remaining_days"] == -2
    assert df.iloc[1]["title"] == "overdue_1"
    assert df.iloc[1]["remaining_days"] == -1

def test_get_overdue_report_when_empty_task_list_raises():
    with pytest.raises(ValueError, match=TaskManager.EMPTY_MESSAGE):
        reports.get_overdue_report([])

def test_get_overdue_report_when_no_overdue_task_raises(sample_task: Task):
    m1 = TaskManager()
    m1.add_task(sample_task)
    with pytest.raises(ValueError, match="Not enough data to report."):
        reports.get_overdue_report(m1.to_dict_list())

def test_get_remaining_reports(task_list: list[dict]):
    df = reports.get_remaining_report(task_list)
    assert  not df.empty
    assert len(df) == 3
    assert df.iloc[0]["title"] == "Test"
    assert df.iloc[0]["remaining_days"] == 1
    assert df.iloc[1]["title"] == "Complete Sample Task"
    assert df.iloc[1]["remaining_days"] == 2
    assert df.iloc[2]["title"] == "Sample Task"
    assert df.iloc[2]["remaining_days"] == 2

def test_get_remaining_report_empty_task_list_raises():
    with pytest.raises(ValueError, match=TaskManager.EMPTY_MESSAGE):
        reports.get_remaining_report([])

def test_get_remaining_report_when_no_remaining_task_raises(overdue_task: Task):
    m1 = TaskManager()
    m1.add_task(overdue_task)
    with pytest.raises(ValueError, match="Not enough data to report."):
        reports.get_remaining_report(m1.to_dict_list())

def test_get_priority_reports_and_sorting_order(task_list: list[dict]):
    df = reports.get_priority_report(task_list)
    assert not df.empty
    assert len(df) == 5
    assert df.iloc[0]["title"] == "Test"
    assert df.iloc[1]["title"] == "Complete Sample Task"
    assert df.iloc[2]["title"] == "overdue_2"
    assert df.iloc[3]["title"] == "overdue_1"
    assert df.iloc[4]["title"] == "Sample Task"

def test_get_priority_report_empty_task_list_raises():
    with pytest.raises(ValueError, match=TaskManager.EMPTY_MESSAGE):
        reports.get_priority_report([])

def test_reports_drop_description_column(task_list: list[dict]):
    df1 = reports.get_overdue_report(task_list)
    df2 = reports.get_remaining_report(task_list)
    df3 = reports.get_priority_report(task_list)
    for df in (df1, df2, df3):
        assert "description" not in df.columns

