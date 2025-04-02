from datetime import datetime, timedelta

def date_range_cython(
    start: datetime, end: datetime, step: timedelta
) -> list[datetime]: ...
