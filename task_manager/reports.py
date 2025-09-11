"""

Report module.

Generates pandas reports from in-memory task records (list[dict]).
"""

import pandas as pd
from . import TaskManager

def remaining_days(df: pd.DataFrame) -> pd.Series:
    """Return days remaining until end date (negative if overdue)."""
    end_date = pd.to_datetime(df["period_end_date"])
    today = pd.Timestamp.today().normalize()
    return (end_date - today).dt.days 

def get_overdue_report(records: list[dict]) -> pd.DataFrame:
    """Overdue tasks (remaining_days < 0), sorted by how overdue they are."""
    df = pd.DataFrame(records)
    if df.empty:
        raise ValueError(TaskManager.EMPTY_MESSAGE)
    df["remaining_days"] = remaining_days(df)
    df = df[df["remaining_days"] < 0].sort_values(["remaining_days", "title"], ascending=[True, True])
    if df.empty:
        raise ValueError("Not enough data to report.")
    df = df.drop(columns=["description"], errors="ignore") # Drop non-report columns
    return df.reset_index(drop=True) 

def get_priority_report(records: list[dict]) -> pd.DataFrame:
    """Tasks sorted by priority (high first), then by nearest end date."""
    df = pd.DataFrame(records)
    if df.empty:
        raise ValueError(TaskManager.EMPTY_MESSAGE)
    df["period_end_date"] = pd.to_datetime(df["period_end_date"])
    df = df.sort_values(["priority","period_end_date", "title"], ascending=[True, True, True])
    df = df.drop(columns=["description"], errors="ignore") # Drop non-report columns
    df["period_end_date"] = df["period_end_date"].dt.strftime("%Y-%m-%d")
    return df.reset_index(drop=True)

def get_remaining_report(records: list[dict]) -> pd.DataFrame:
    """Non-overdue tasks with remaining_days >= 0, sorted soonest first."""
    df = pd.DataFrame(records)
    if df.empty:
        raise ValueError(TaskManager.EMPTY_MESSAGE)
    df["remaining_days"] = remaining_days(df)
    df = df[df["remaining_days"] >= 0].sort_values(["remaining_days", "title"], ascending=[True, True])
    if df.empty:
        raise ValueError("Not enough data to report.")
    df = df.drop(columns=["description"], errors="ignore") # Drop non-report columns
    return df.reset_index(drop=True)
 