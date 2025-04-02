#!/usr/bin/env python3
"""
Examples of using the date_range functionality in ctime.
This example shows how to work with date ranges and intervals.
"""
from datetime import datetime, timedelta

from libs.ctime.ctime.ranges import get_daily_date_range as date_range


def demonstrate_basic_range():
    """Show basic date range usage."""
    print("Basic Date Range Example:\n")

    # Create a date range for the next 5 days
    start_date = datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    end_date = start_date + timedelta(days=5)

    print(f"Dates from {start_date.date()} to {end_date.date()}:")
    for date in date_range(start_date, end_date):
        print(f"  - {date.date()}")


def demonstrate_custom_interval():
    """Show date range with custom intervals."""
    print("\nCustom Interval Example (every 2 days):\n")

    # Create a date range with 2-day intervals
    start_date = datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    end_date = start_date + timedelta(days=10)
    step = timedelta(days=2)

    print(
        f"Dates from {start_date.date()} to {end_date.date()} (2-day intervals):"
    )
    for date in date_range(start_date, end_date, step):
        print(f"  - {date.date()}")


def demonstrate_month_range():
    """Show how to create a range spanning months."""
    print("\nMonth Range Example:\n")

    # Create a range spanning multiple months
    start_date = datetime.now().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    end_date = (start_date + timedelta(days=60)).replace(day=1)

    print(
        f"First day of each month from {start_date.date()} to {end_date.date()}:"
    )
    current = start_date
    while current < end_date:
        print(f"  - {current.date()}")
        # Move to first of next month
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)


if __name__ == "__main__":
    demonstrate_basic_range()
    demonstrate_custom_interval()
    demonstrate_month_range()
