"""

Task model.

Stores task data, validates fields (dates, priority, status), and supports:
- Status helpers (marked_complete, marked_not_started, mark_in_progress)
- Serialization (to_dict / from_dict)
- User-friendly formatting (__str__/__repr__)
"""

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
        status (str): Completion status (c = Completed, ns = Not Started, inp = In-progress, default to 'ns').
    """
    # Maps numeric priority to readable text (used in displays)
    PRIORITY_MAP = {1: "highest", 2: "high", 3: "medium", 4: "low", 5: "lowest"}
    # Maps short status codes to readable text
    STATUS_MAP = {"c": "completed", "ns":"not started", "inp":"in-progress"}

    def __init__(
            self, 
            title: str,  
            period_end_date: str | date,
            period_start_date: str | date = date.today(), 
            priority: int = 3, 
            status: str = "ns",
            description: str = "",   
        ):
        self.title = title
        self.description = description
        self.period_start_date = period_start_date
        self.period_end_date = period_end_date
        self.priority = priority
        self.status = status
    
    def __eq__(self, other: object) -> bool:
        """Check this Task is equal to another Task by comparing all attributes."""
        if not isinstance(other, Task):
            return NotImplemented
        return (
            self.title == other.title and
            self.period_start_date == other.period_start_date and
            self.period_end_date == other.period_end_date and
            self.priority == other.priority and
            self.status == other.status and
            self.description == other.description
        )
    
    def __repr__(self) -> str:
        """Developer-friendly representation (safe for debugging)."""
        return (
            f"Task(title={self.title!r},"
            f"period_start_date={self.period_start_date},"
            f"period_end_date={self.period_end_date},"
            f"priority={self.priority},"
            f"status={self.status!r},"
            f"description={self.description!r})"
        )
    
    def __str__(self) -> str:
        """Return a user-friendly string with task details."""
        status_text = type(self).STATUS_MAP.get(self.status, str(self.status)).title()
        priority_text = type(self).PRIORITY_MAP.get(self.priority, str(self.priority)).title()
        description_text = self.description or "(No Description)"
        labels = {
            "Status": status_text,
            "Priority": priority_text,
            "Description": description_text
        }
        # Find the longest label for alignment
        max_label_len = max(len(label) for label in labels.keys())
        # Build the aligned string
        details = "\n".join(f"{label.ljust(max_label_len)} : {value.title()}" for label, value in labels.items())
        return f"{self.title} ({self.period_start_date} - {self.period_end_date})\n{details}"
    
    def marked_complete(self) -> None:
        """Mark the task as completed."""
        self.status = "c"

    def marked_not_started(self) -> None:
        """Mark the task as not started."""
        self.status = "ns"
    
    def mark_in_progress(self) -> None:
        """Mark the task as in-progress"""
        self.status = "inp"
    
    def is_overdue(self) -> bool:
        """Return True if the current date is after the task's end date."""
        return date.today() > self.period_end_date


    def to_dict(self) -> dict:
        """Convert Task to dictionary for export"""
        return {
            "title": self.title,
            "period_start_date": self.period_start_date.isoformat(),
            "period_end_date": self.period_end_date.isoformat(),
            "priority": self.priority,
            "status": self.status,
            "description": self.description,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Rebuild Task from a dictionary. Expects ISO date strings"""
        return cls(
            title = data["title"],
            period_start_date = date.fromisoformat(data["period_start_date"]),
            period_end_date = date.fromisoformat(data["period_end_date"]),
            priority = data["priority"],
            status = data["status"],
            description = data.get("description", ""),
        )
    
# ---- Validators ----

    @staticmethod
    def validate_title(value: str) -> str:
        """Ensure the title is not empty or whitespace."""
        if not value.strip():
            raise ValueError("Title can't be empty.")
        return value.strip()
    
    @staticmethod
    def validate_date(value: str | date) -> date:
        """Accept a date object or a YYYY-MM-DD string and check valid date format: YYYY-MM-DD"""
        try:
            return datetime.strptime(str(value), "%Y-%m-%d").date()
        except ValueError: 
            raise ValueError("Please Enter a valid date in YYYY-MM-DD format.")

    @staticmethod       
    def validate_date_order(start: date, end: date) -> None:
        """Ensure end date is not before start date."""
        if end < start:
            raise ValueError("End date must be greater than or equal to start date.")
    
    @classmethod    
    def validate_priority(cls, value: int) -> int:
        """Validate that the priority is an integer between 1 and 5."""
        value = int(value)
        if value not in cls.PRIORITY_MAP:
            raise ValueError("Priority must be numeric and between 1 and 5.")
        return value
    
    @classmethod
    def validate_status(cls, value: str) -> str:
        """Validate and normalize the status value."""
        value = value.strip().lower()
        for dict_key, dict_value in cls.STATUS_MAP.items(): 
            if value == dict_key or value == dict_value:
                return dict_key # normalize to short form
        raise ValueError ("Use c (Completed), ns (Not Started), or inp (In-progress).") 

# ---- Property and setters ----

    @property
    def title(self): 
        return self._title
    @title.setter
    def title(self, value: str): 
        self._title = self.validate_title(value)

    @property
    def period_start_date(self): 
        return self._period_start_date
    @period_start_date.setter
    def period_start_date(self, value: str | date):
        self._period_start_date = self.validate_date(value)
        if hasattr(self, "_period_end_date"):
            self.validate_date_order(self._period_start_date, self.period_end_date)
    
    @property
    def period_end_date(self):
        return self._period_end_date
    @period_end_date.setter
    def period_end_date(self, value: str | date):
        self._period_end_date = self.validate_date(value)
        if hasattr(self, "_period_start_date"):
            self.validate_date_order(self.period_start_date, self._period_end_date)
    
    @property
    def priority(self):
        return self._priority 
    @priority.setter
    def priority(self, value: int):
        self._priority = self.validate_priority(value)
        
    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, value: str):
        self._status = self.validate_status(value)
    
    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        self._description = value or ""

        

