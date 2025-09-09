"""

Task manager core.

Provides TaskManager: in-memory CRUD for Task objects, list/view helpers, 
and simple serialization for FileIO.
"""

from .task import Task

class TaskManager:
    """Represents a Task Manager."""
    EMPTY_MESSAGE = "There is no task. Please add a task."

    def __init__(self):
        self.tasks: list[Task] = []
        

    def add_task(self, task: Task) -> str:
        """Adds a task in the tasks list."""
        if task is None:
            raise ValueError("Task object can't be None.")
        self.tasks.append(task)
        return f"Task '{task.title}' has been added successfully."

    def delete_task(self, number: int) -> str:
        """Delete a task by its number."""
        number = self.validate_index(number)
        delete = self.tasks.pop(number-1)
        return f"Task '{delete.title}' has been deleted successfully."
    
    def update_task(self, number: int, task: Task) -> str:
        """Updates a particular task by its number"""
        if task is None:
            raise ValueError("Task object can't be None.")
        number = self.validate_index(number)
        self.tasks[number-1] = task
        return f"Task '{task.title}' updated successfully."
    
    # TODO improve ui design with 'rich' or 'tabulate' in next version. 
    def view_tasks(self):
        """View all the tasks in a file."""
        if not self.tasks:
            raise ValueError(self.EMPTY_MESSAGE)
        for i, task in enumerate(self.tasks):
            yield f"{i + 1}. {task}"

    def to_dict_list(self) -> list[dict]:
        """Convert the list of Task objects to a list of dictionaries."""
        return [task.to_dict() for task in self.tasks]

# ---- Validations ----

    def validate_index(self, number: int) -> int:
        """Validate a task number and return it as int."""
        if not self.tasks:
            raise ValueError(self.EMPTY_MESSAGE)
        try: 
            number = int(number) 
        except ValueError: 
            raise ValueError("Please enter a valid number.")
        if not(1 <= number <= len(self.tasks)):
            raise ValueError(f"Please enter a number between 1 and {len(self.tasks)}.")
        return number
        