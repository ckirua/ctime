from datetime import datetime, timedelta


def get_daily_date_range(
    start_date: datetime, end_date: datetime, delta: timedelta = timedelta(days=1)
) -> list[datetime]:
    return [start_date + delta * i for i in range((end_date - start_date).days + 1)]
