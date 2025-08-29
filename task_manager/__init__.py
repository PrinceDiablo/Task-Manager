#task_manager.py
from task import Task

class TaskManager:
    """Represents a Task Manager."""

    def __init__(self):
        self.tasks: list[Task] = []
        

    def add_task(self, task: Task) -> str:
        """Adds a task and return confirmation."""
        self.tasks.append(task)
        return f"Task '{task.title}' has been added successfully."

    def delete_task(self, number: int) -> str:
        """Delete a task by its number and return confirmation."""
        delete = self.tasks.pop(number-1)
        return f"Task '{delete.title}' has been deleted successfully."
    
    def update_task(self, number: int, task: Task) -> str:
        """Updates a particular task by its number"""
        self.tasks[number-1] = task
        return f"Task '{task.title}' updated successfully."
    # TODO need to improve this function
    def view_tasks(self):
        """View all the tasks in a file."""
        for i, task in enumerate(self.tasks):
            yield f"{i + 1}. {task}"

    def to_dict_list(self) -> list[dict]:
        """Convert the list of Task objects to a list of dictionaries."""
        return [task.to_dict() for task in self.tasks] 