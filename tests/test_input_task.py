"""

InputTask tests.

Covers defaults on blanks, and reprompts for invalid inputs.
"""

import builtins
from datetime import date, timedelta
from ui.cli.input_task import InputTask
from task_manager.task import Task

def test_input_task_all_fields_filled(monkeypatch):
    today = date.today()
    inputs = iter([
        "Title",            # title
        "Description",      # description
        today.isoformat(),  # start date
        (today + timedelta(days=2)).isoformat(), # end date
        "4",                # priority
        "inp",              # status
    ])
    monkeypatch.setattr(builtins, "input", lambda *_: next(inputs))
    t = InputTask.input_task()
    assert isinstance(t, Task)
    assert t.title == "Title"
    assert t.period_start_date == today
    assert t.period_end_date == today + timedelta(days=2)
    assert t.priority == 4
    assert t.status == "inp"
    assert t.description == "Description"

def test_input_task_defaults_on_blank(monkeypatch):
    today = date.today()
    inputs = iter([
        "Title",        # title
        "",             # description
        "",             # start date
        (today + timedelta(days=1)).isoformat(), # end date
        "",             # priority
        ""              # status
    ])
    monkeypatch.setattr(builtins, "input", lambda*_: next(inputs))
    t = InputTask.input_task()
    assert t.period_start_date == today
    assert t.priority == 3
    assert t.status == "ns"
    assert t.description == ""

def test_input_task_reprompt_on_bad_end_date(monkeypatch, capsys):
    today = date.today()
    inputs = iter([
        "Title",            # title
        "",                 # description
        today.isoformat(),  # start date
        (today - timedelta(days=1)).isoformat(), # invalid end date(before start)
        (today + timedelta(days=1)).isoformat(), # valid end date
        "3",                # priority
        "ns",               # status
    ])
    monkeypatch.setattr(builtins, "input", lambda*_: next(inputs))
    t = InputTask.input_task()
    out = capsys.readouterr().out
    assert "Invalid Input" in out
    assert t.period_end_date == today + timedelta(days=1)

def test_valid_input_required_field_reprompts_on_blank(monkeypatch, capsys):
    calls = iter(["","Title"])
    monkeypatch.setattr(builtins,"input", lambda*_:next(calls))
    result = InputTask.valid_input("Title*: ", Task.validate_title)
    assert result == "Title"
    assert "this field is required" in capsys.readouterr().out.lower()

def test_input_task_reprompt_on_invalid_date_format(monkeypatch, capsys):
    today = date.today()
    inputs = iter([
        "Title",            # title
        "",                 # description
        today.isoformat(),  # start date
        "bad-date",         # invalid format -> triggers valid_input except  
        "57",               # still invalid(not YYYY-MM-DD)
        (today + timedelta(days=1)).isoformat(), # valid end date
        "3",                # priority
        "ns"                # status
    ])
    monkeypatch.setattr(builtins, "input", lambda*_:next(inputs))
    t = InputTask.input_task()
    out = capsys.readouterr().out
    assert "Invalid Input" in out
    assert t.period_end_date == today + timedelta(days=1)

def test_input_task_reprompt_on_invalid_priority(monkeypatch, capsys):
    today = date.today()
    inputs = iter([
        "Title",    # title
        "",         # description
        "",         # start date
        (today + timedelta(days=1)).isoformat(), # end date
        "status",   # invalid priority -> triggers except
        "6",        # still invalid (>5)
        "3",        # valid
        "ns"        # status
    ])
    monkeypatch.setattr(builtins, "input", lambda*_:next(inputs))
    t = InputTask.input_task()
    out = capsys.readouterr().out
    assert "Invalid Input" in out
    assert t.priority == 3

def test_input_task_reprompt_on_invalid_status(monkeypatch, capsys):
    today = date.today()
    inputs = iter([
        "Title",    # title
        "",         # description
        "",         # start date
        (today + timedelta(days=1)).isoformat(), # end date
        "3",        # priority
        "done",     # invalid status
        "c",        # valid
    ])
    monkeypatch.setattr(builtins, "input", lambda *_: next(inputs))
    t = InputTask.input_task()
    out = capsys.readouterr().out.lower()
    assert "invalid input" in out
    assert t.status == "c"

    
