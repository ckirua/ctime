from datetime import datetime, timedelta

import numpy as np

def datetime_range(
    start: datetime, end: datetime, step: timedelta
) -> list[datetime]: ...
def timestamp_s_range(
    start: datetime, end: datetime, step: timedelta
) -> np.ndarray[np.int64]: ...
