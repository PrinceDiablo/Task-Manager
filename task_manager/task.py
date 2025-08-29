# task.py
from datetime import datetime, date 

class Task:
    """
    Represents a task with a title, description, time period, priority and completion status.
    
    Attributes:
        title (str): Short name of the task.
        description (str): Detailed explanation of the task (defaults to blank).
        period_start_date (date): Start date (defaults to today).
        period_end_date (date): Target completion date.
        priority (int): Priority level (1 = Highest, 2 = High, 3 = Medium, 4 = low, 5 = lowest, default to 3).
        status (str): Completion status (c = Completed, nc = Not Completed, inp = In-progress, default to 'nc').
    """
    PRIORITY_MAP = {1: "Highest", 2: "High", 3: "Medium", 4: "low", 5: "lowest"}
    STATUS_MAP = {"c": "completed", "nc":"not started", "inp":"in-progress"}

    def __init__(
            self, 
            title: str,  
            period_end_date: date, 
            priority: int = 3, 
            status: str = "nc",
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
        self.status = "c"

    def marked_not_started(self) -> None:
        """Mark the task as not started."""
        self.status = "nc"
    
    def mark_in_progress(self) -> None:
        """Mark the task as in-progress"""
        self.status = "inp"
    
    def is_overdue(self) -> bool:
        """Return True if the current date is after the task's end date."""
        return date.today() > self.period_end_date

    def __repr__(self) -> str:
        """Return a developer-friendly string representation of the task."""
        return (
            f"Task(title='{self.title}', "
            f"period_end_date={self.period_end_date},"
            f"priority={self.priority}, "
            f"status={self.status})"
        )
    
    def __str__(self) -> str:
        """Return a user-friendly string with task details."""
        labels = {
            "Status": type(self).STATUS_MAP.get(self.status),
            "Priority": type(self).PRIORITY_MAP.get(self.priority),
            "Description": self.description or "(No description)"
        }

        # Find the longest label for alignment
        max_label_len = max(len(label) for label in labels.keys())

        # Build the aligned string
        details = "\n".join(f"{label.ljust(max_label_len)} : {value}" for label, value in labels.items())

        return f"{self.title} ({self.period_start_date} - {self.period_end_date})\n{details}"

    def to_dict(self) -> list[dict]:
        """Convert Task to list of dictionarys for export"""
        return {
            "title": self.title,
            "description": self.description,
            "period_start_date": self.period_start_date.isoformat(),
            "period_end_date": self.period_end_date.isoformat(),
            "priority": self.priority,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: list[dict]) -> "Task":
        """Rebuild Task from a list of dictionarys."""
        return cls(
            title = data["title"],
            description = data.get("description", ""),
            period_start_date = date.fromisoformat(data["period_start_date"]),
            period_end_date = date.fromisoformat(data["period_end_date"]),
            priority = data["priority"],
            status = data["status"]
        )
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value: str):
        if not value.strip():
            raise ValueError("This field can't be empty.")
        self._title = str(value)
    
    def _date_check(self, value: str, attribute_name: str) -> date:
        """Checks valid date format: YYYY-MM-DD"""
        try:
            date_obj = datetime.strptime(str(value), "%Y-%m-%d").date()
            setattr(self, attribute_name, date_obj)
        except ValueError:
            raise ValueError("Please Enter a valid date in YYYY-MM-DD format.")

    @property
    def period_start_date(self):
        return self._period_start_date
    
    @period_start_date.setter
    def period_start_date(self, value: str):
        self._date_check(value, "_period_start_date")
    
    @property
    def period_end_date(self):
        return self._period_end_date
    
    @period_end_date.setter
    def period_end_date(self, value: str):
        self._date_check(value, "_period_end_date")
    
    @property
    def priority(self):
        return self._priority
    
    @priority.setter
    def priority(self, value: int):
        try:
            value = int(value)
            if value not in type(self).PRIORITY_MAP.keys():
                raise ValueError ("Priority must be 1 for highest, 2 for High, 3 for Medium, 4 for Low, 5 for Lowerst.")
            self._priority = value # Values stored in the class are : 1 to 5
        except ValueError:
            raise ValueError("Please enter a number.")
        
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value: str):
        value = value.strip().lower()
        for k, v in type(self).STATUS_MAP.items(): # k = dictionary key and v = dictionary value
            if v == value or k == value:
                self._status = k # Values stored in the class are: c, nc, inp 
                return
        raise ValueError ("Invalid Choice. Use Completed(c) or Not Completed(nc) or In-progress(inp).") 

        

