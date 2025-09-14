"""

Test Task Manager CLI entry point.

Unit tests for Task Manager CLI entry point: Behavior.
"""

import main
from task_manager import TaskManager, Task

def test_input_other_choices(capsys):
    inputs = iter([
        "",         # invalid input
        "odd",      # still invalid
        "add",      # valid input
    ])
    result = main.input_other_choices(input_fn=lambda *_: next(inputs))
    out = capsys.readouterr().out
    assert "Please enter a valid option:" in out
    assert result == "add" 

def test_input_create_open(capsys):
    inputs = iter([
        "",             # invalid input
        "crote",        # still invalid
        "create"        # valid input
    ])
    result = main.input_create_open(input_fn=lambda *_: next(inputs))
    out = capsys.readouterr().out
    assert "Please enter a valid option:" in out
    assert result == "create"

def test_input_aliases():
    assert main.input_other_choices(input_fn=lambda *_: "a") == "a"
    assert main.input_create_open(input_fn=lambda *_: "o") == "o"

def test_update_delete_helper(capsys):
    m1 = TaskManager()
    t = Task("Title", "2025-09-15")
    m1.add_task(t)
    # valid on first try
    result = main.update_delete_helper("prompt", m1, input_fn=lambda _: "1")
    assert result == 1
     # invalid then valid
    inputs = iter([
        "0",        # invalid input
        "2",        # still invalid
        "1"         # valid input
    ])
    result = main.update_delete_helper("prompt", m1, input_fn=lambda *_: next(inputs))
    out = capsys.readouterr().out.lower()
    assert "invalid" in out or "please enter" in out
    assert result == 1

def test_update_delete_helper_empty_manager(capsys):
    m = TaskManager()
    result = main.update_delete_helper("prompt", m, input_fn=lambda *_: "1")
    out = capsys.readouterr().out
    assert result is None
    assert TaskManager.EMPTY_MESSAGE in out
