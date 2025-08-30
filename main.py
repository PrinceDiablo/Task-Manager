"""
main.py
---------
Entry point for the Task Manager CLI. 
Handles user interaction, menus, and delegates work to manager and FileIO.
"""

from task_manager import TaskManager, Task
from task_manager.fileio import json_io, csv_io, FileIO
from pathlib import Path
from ui.cli.input_task import InputTask 
import sys

manager = TaskManager()

def main():
    """Run the Task Manager CLI loop (create/open and handle user choices)."""

    print("\n" + "*"*10 + " Welcome to Task-Manager " + "*"*10 + "\n")
    print("(...) are keywords that can be used in CLI.\n")
    
    path = ""
    initial_choice = input_create_open()
    if initial_choice in ("create", "c"):
        print("\nPlease add your first task:\n")
        print("\n"+ manager.add_task(InputTask.input_task()))   
    elif initial_choice in ("open", "o"):
        path = input("Please enter the file path you wish to open: ")
        print("\n" +"*"*10)
        try:
            data = FileIO.import_(Path.suffix(path) ,path)
        except (FileNotFoundError, ValueError):
            print("Error: No such file exists.")
        for item in data:
            print(manager.add_task(Task.from_dict(item)))
        print("File imported succesfully")
        if input("Do you wish to see the content of the file(y/n): ").strip().lower() in ("yes", "no"):
            for task in manager.view_tasks():
                print(task)
        print("*"*10) 

    while True:
        choice = input_other_choices()
        path = other_choices(choice, manager, path)


def other_choices(choice: str, manager: TaskManager, path: str) -> str:        
    match choice:
    # ---- Save and Exit Options ----
        # TODO auto-save feature
        # Save Option:
        case "save" | "s":
            if not path:
                path = input("Please enter a file path where you want to save: ")
            try:
                print(FileIO.export(Path(path).suffix, manager.to_dict_list(), path))
                return path
            except (FileNotFoundError, ValueError):
                print("\nError: No such path or file exists.")
        
        # Save as Option:
        case "save_as" | "sa":
            new_path = input("Please enter a file path where you want to save: ")
            try:               
                print(FileIO.export(Path(path).suffix, manager.to_dict_list(), new_path))
                if not path:
                    return new_path
            except (FileNotFoundError, ValueError):
                print("Error: No such path or file exists.")

        # Save and Exit Option:   
        case "save_exit" | "se":
            if not path:
                path = input("Please enter a file path where you want to save: ")
            try:               
                print(FileIO.export(Path(path).suffix, manager.to_dict_list(), path))
                return path
            except (FileNotFoundError, ValueError):
                print("Error: No such path or file exists.")
            print("Thank You, see you soon")
            sys.exit(0)
        
        # Exit Option:
        case "exit" | "q":
            if input("Why don't you stay a little longer(y/n): ").strip().lower() in ("no", "n"):
                print("Haa, Haa, Haa, how was it, see you soon")
                sys.exit(0)
            else:
                print("Why typing useless options. Focus on your work.")

    # ---- Modifying Task Options ----   
     
        # Add Task Option:
        case "add" | "a":
            print(manager.add_task(InputTask.input_task()))
        
        # Edit Task Option:
        case "edit" | "e":
            number = update_delete_helper("Which task number would you like to update? ")
            print(manager.tasks[number-1])
            print(manager.update_task(number, InputTask.input_task()))
        
        #Update Status Option:
        case "update_status" | "u":
            number = update_delete_helper("Which task number would you like to update? ")
            #TODO proper status update logic
        
        #View Task Option: TODO improve ui design may be later with 'rich' or 'tabulate'
        case "view" | "v":
            for task in manager.view_tasks():
                print(task)
        
        #Delete Task Option:
        case "delete" | "del":
            number = update_delete_helper("Which task number do you want to delete? ")
            if input(f"Are you sure you want to delete task no. {number} (y/n): ").strip().lower() in ("yes", "y"):
                print(manager.delete_task(number))
        
    # ---- Report View options ---- TODO (not implemented yet)

        case "overdue" | "d":
            # TODO
            print("Report Section (Comming Soon)")
        case "priority" | "p":
            # TODO
            print("Report Section (Comming Soon)")
        case "remaining" | "r":
            # TODO
            print("Report Section (Comming Soon)")
        
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
    

if __name__ == "__main__":
    main()
