"""
main.py
---------
Entry point for the Task Manager CLI. 
Handles user interaction, menus, and delegates work to manager and FileIO.
"""

from task_manager import TaskManager
from task_manager.task import Task
from task_manager.fileio import FileIO
from pathlib import Path
from datetime import datetime, date
import sys

manager = TaskManager()

def main():
    """Run the Task Manager CLI loop (create/open and handle user choices)."""
    print("\n" + "*"*10 + " Welcome to Task-Manager " + "*"*10 + "\n")
    print("(...) are keywords that can be used in CLI.\n")
    
    path = ""
    choice1 = input_create_open()
    if choice1 in ("create", "c"):
        print("\nPlease add your first task:\n")
        print(manager.add_task(input_task()))   
    elif choice1 in ("open", "o"):
        path = input("Please enter the file path you wish to open: ")
        print("\n" +"*"*10)
        data = FileIO.import_(Path.suffix(path) ,path)
        for item in data:
            print(manager.add_task(Task.from_dict(item)))
        print("File imported succesfully")
        # TODO need to improve this view also
        if input("Do you wish to see the content of the file(y/n): ").strip().lower() in ("yes", "no"):
            for _ in manager.tasks:
                print(manager.view_tasks)
        print("*"*10) 

    while True:
        choice2 = input_other_choices()
        other_choices(choice2, manager, path)


def other_choices(choice, manager, path):        
    match choice:
        case "save" | "s":
            if not path:
                path = input("Please enter a file path where you want to save: ")               
            print(FileIO.export(Path.suffix(path), manager.to_dict_list(), path))
        case "save_as" | "sa":
            new_path = input("Please enter a file path where you want to save: ")               
            print(FileIO.export(Path.suffix(path), manager.to_dict_list(), new_path))
            if not path:
                path = new_path
        case "save_exit" | "se":
            if not path:
                path = input("Please enter a file path where you want to save: ")               
            print(FileIO.export(Path.suffix(path), manager.to_dict_list(), path))
            print("Thank You, see you soon")
            sys.exit(0)
        case "exit" | "q":
            if input("Why don't you stay a little longer(y/n): ").strip().lower() in ("no", "n"):
                print("Haa, Haa, Haa, how was it, see you soon")
                sys.exit(0)
            else:
                print("Why typing useless options. Focus on your work.")
        case "add" | "a":
            print(manager.add_task(input_task()))
        case "edit" | "e":
            number = update_delete_helper("Which task number would you like to update? ")
            print(manager.tasks[number-1])
            print(manager.update_task(number, input_task()))
        case "update_status" | "u":
            number = update_delete_helper("Which task number would you like to update? ")
            #TODO proper status update logic
        case "view" | "v": # TODO need to update view 
            for _ in manager.tasks:
                print(manager.view_tasks())
        case "delete" | "del":
            number = update_delete_helper("Which task number do you want to delete? ")
            if input(f"Are you sure you want to delete task no. {number} (y/n): ").strip().lower() in ("yes", "y"):
                print(manager.delete_task(number))
        case "overdue" | "d":
            ...
        case "priority" | "p":
            ...
        case "remaining" | "r":
            ...
        
def update_delete_helper(prompt) -> int:
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(manager.tasks):
                return choice
            print(f"Please enter a number between 1 and {len(manager.tasks)}.")
        except ValueError:
            print("Please enter a valid number.")
        
# TODO need to move all inputs
def input_other_choices() -> str:
    """Prompt the user for an action (add, update, delete, etc.) and return the normalized keyword."""
    choices = ["add", "a", "edit", "e", "update_status", "u", "delete", "del" , "view", "v", "overdue", "d", 
               "priority", "p", "remaining", "r", "save", "s", "save_as", "sa","save_exit", "se","exit","q"]
    print()
    print("*"*10)
    print("What do you want to do now? Options Are:")
    print("(Add) more task, (edit) task, (update) status of the task, (delete) task, (view) all tasks,")
    print("view (overdue) tasks, sort by (priority), sort by least time (remaining).")
    print("(save) to csv or json, save to new location (save_as),save and exit(save_exit), (exit)")
    print("*"*10)

    while True:
        choice = input("Enter your Choice: ").strip().lower()
        if choice in choices:
            return choice
        print("Please enter a valid choice:\n " \
            "add(a), edit(e), update_status(u), delete(del), view(v), overdue(d),\n" \
            "priority(p), remaining(r), save(s), save_as(sa), save_exit(sq), exit(q): ")

def input_create_open() -> str:
    """Prompt the user for creating or opening a file."""
    choices = ["create", "c", "open", "o"]
    while True:
        choice = input("Do you want to (Create) a List or (Open) an existing list? ").strip().lower()
        if choice in choices:
            return choice
        print()
        print("Please enter a valid option: c to Create, o to Open.")
# TODO need to move to input_task.py
def valid_input(prompt: str, condition, allow_blank=False, default=None):
    """Validated each user input"""
    while True:
        raw = input(prompt).strip()
        if not raw:
            if allow_blank: # blank -> return default
                return default
            print("This field is required. Please enter a value.")
            continue
        try:
            return condition(raw)
        except ValueError as e:
            print(f"Invalid Input: {e}")

def valid_date(value: str) -> date:
        """Checks valid date format: YYYY-MM-DD"""
        try:
            datetime.strptime(value, "%Y-%m-%d").date()
            return value
        except ValueError:
            raise ValueError("Valid date format is YYYY-MM-DD")

def input_task() -> Task:
    """Collect user input for creating a Task object."""
    title_ = valid_input("Title*: ", str) #required
    description_ = input("Description (Enter to skip): ").strip()
    period_start_date_ = valid_input(
        "Period_start_date: YYYY-MM-DD (Enter to skip): ", 
        valid_date, 
        allow_blank=True,
        default=date.today()
    )
    period_end_date_ = valid_input("Period_end_date*: YYYY-MM-DD: ", valid_date) #required
    priority_ = valid_input(
        "Priority(1=highest, 2=High, 3=Medium, 4=Low, 5=Lowerst) (Enter to skip): ",
        lambda s: int(s) if int(s) in range(1, 6) 
                    else (_ for _ in ()).throw(ValueError("Priority must be between 1 and 5")),
        allow_blank=True,
        default=3
    )
    status_ = valid_input(
        "Status: c for Completed, nc for Not Completed, inp for In-progress (Enter to skip): ",
        lambda s: str(s).lower() if s in Task.STATUS_MAP.keys() or s in Task.STATUS_MAP.values() 
                    else (_ for _ in ()).throw(ValueError("Status must be c for Completed, nc for Not Completed, inp for In-progress")),
        allow_blank=True,
        default="nc"
    )
    return Task(
        title=title_,
        description=description_,
        period_start_date=period_start_date_,
        period_end_date=period_end_date_,
        priority=priority_,
        status=status_ 
    )
    

if __name__ == "__main__":
    main()
