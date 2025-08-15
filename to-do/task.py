
from datetime import date 

class Task():
    """
    Represents a task with a title, description, time period, priority and completion status.
    
    Attributes:
        title (str): Short name of the task.
        description (str): Detailed explanation of the task (defaults to blank).
        period_start_date (date): Start date (defaults to today).
        period_end_date (date): Target completion date.
        priority (int): Priority level (1 = high, 2 = medium, 3 = low).
        status (bool): Completion status (False = not completed, True = completed).
    """
    PRIORITY_MAP = {1: "High", 2: "Medium", 3: "Low"}

    def __init__(
            self, 
            title: str,  
            period_end_date: date, 
            priority: int, 
            status: bool = False,
            description: str = "", 
            period_start_date: date = date.today()
        ):
        self.title = title
        self.description = description
        self.period_start_date = period_start_date
        self.period_end_date = period_end_date
        self.priority = priority
        self.status = status
    
    def marked_complete(self) -> None:
        """Mark the task as completed."""
        self.status = True

    def marked_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.status = False
    
    def is_overdue(self) -> bool:
        """
        Checks if the task is past its end date.

        Returns:
            bool: True if if the current date is after the period_end_date, False otherwise.
        """
        return date.today() > self.period_end_date

    def __repr__(self) -> str:
        """
        Developer-friendly representation of the Task.

        Returns:
            str: Constructer-like representation.
        """
        return (
            f"Task(title ='{self.title}', "
            f"period_end_date = {self.period_end_date} ,"
            f"priority = {self.priority}, "
            f"status={self.status})"
        )
    
    def __str__(self) -> str:
        """
        Human-readable detailed task description.

        Returns:
            str: Multi-line formatted task details.
        """
        labels = {
            "Status": "Completed" if self.status else "Not Completed",
            "Priority": type(self).PRIORITY_MAP.get(self.priority, "Unknown"),
            "Description": self.description or "(No description)"
        }
        
        # Find the longest label for alignment
        max_label_len = max(len(label) for label in labels.keys())

        # Build the aligned string
        details = "\n".join(f"{label.ljust(max_label_len)} : {value}" for label, value in labels.items())

        return f"{self.title} ({self.period_start_date} - {self.period_end_date})\n{details}"
