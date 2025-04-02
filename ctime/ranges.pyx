from cpython.datetime cimport datetime, timedelta
import numpy as np
cimport numpy as cnp

# Numpy must be initialized
cnp.import_array()

def get_daily_timestamps(
    start_date: datetime,
    end_date: datetime,
    delta: timedelta = None
) -> np.ndarray:
    if delta is None:
        delta = timedelta(days=1)
    
    cdef int total_days = (end_date - start_date).days + 1
    cdef double[:] result = np.empty(total_days, dtype='float64')
    cdef int i
    cdef double ts = start_date.timestamp()
    cdef double delta_seconds = delta.total_seconds()
    
    for i in range(total_days):
        result[i] = ts
        ts += delta_seconds
    
    return np.asarray(result)
    
cpdef list[datetime] get_daily_date_range(datetime start_date, datetime end_date, timedelta delta=timedelta(days=1)):
    cdef int i
    cdef list[datetime] result = []
    cdef int days_diff = (end_date - start_date).days + 1
    
    for i in range(days_diff):
        result.append(start_date + delta * i)
    
    return result


# Vectorized version with proper Cython optimizations
def get_daily_timestamps_vectorized(
    start_date: datetime,
    end_date: datetime,
    delta: timedelta = None
) -> cnp.ndarray:
    if delta is None:
        delta = timedelta(days=1)
    
    cdef:
        int total_days = (end_date - start_date).days + 1
        double ts = start_date.timestamp()
        double delta_seconds = delta.total_seconds()
        cnp.ndarray[cnp.float64_t] result
    
    # Use numpy's arange with C-contiguous output
    result = ts + delta_seconds * np.arange(total_days, dtype=np.float64)
    return result

