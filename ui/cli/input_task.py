#input_task.py
from task_manager import Task
from datetime import date

class InputTask:
    """Help validate and input task, one field at a time."""

    @staticmethod
    def valid_input(prompt: str, validator, allow_blank=False, default=None):
        """Validated each user input"""
        while True:
            value = input(prompt).strip()
            if not value:
                if allow_blank: # if blank -> return default
                    return default
                print("This field is required. Please enter a value.")
                continue
            try:
                return validator(value)
            except ValueError as e:
                print(f"Invalid Input: {e}")

    @classmethod
    def input_task(cls) -> Task:
        """Collect user input for creating a Task object."""
        #Title Field (required)
        title = cls.valid_input(
            "Title*: ", 
            Task.validate_title
        ) 
        #Descrption Field
        description = input("Description (Enter to skip): ").strip()
        #Period_start_date Field
        start_date = cls.valid_input(
            "Period_start_date (YYYY-MM-DD, Enter to skip): ", 
            Task.validate_date, 
            allow_blank=True,
            default=date.today()
        )
        # Period_end_date Field (required)
        while True:
            end_date = cls.valid_input(
                "Period_end_date* (YYYY-MM-DD): ",
                Task.validate_date
            ) 
            if end_date >= start_date:
                break
            print("Invalid Input: End date must be greater than or equal to start date.")          
        # Priority Field     
        priority = cls.valid_input(
            "Priority(1=highest, 2=High, 3=Medium, 4=Low, 5=Lowerst, Enter to skip): ",
            Task.validate_priority,
            allow_blank=True,
            default=3
        )
        # Status Field
        status = cls.valid_input(
            "Status (c for Completed, nc for Not Completed, inp for In-progress, Enter to skip): ",
            Task.validate_status,
            allow_blank=True,
            default="nc"
        )
        
        return Task(title,end_date,start_date,priority,status,description)