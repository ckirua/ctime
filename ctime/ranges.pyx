import numpy as np
from cpython.datetime cimport datetime, timedelta
from cpython.list cimport PyList_New, PyList_SET_ITEM
from cpython.ref cimport Py_INCREF
from cython.parallel import prange
from libc.math cimport floor
from libc.stdint cimport int64_t
cimport numpy as cnp


cpdef list datetime_range(datetime start, datetime end, timedelta step):
    cdef:
        int n = int((end - start).total_seconds() / step.total_seconds()) + 1
        list dates = PyList_New(n)
        datetime current = start
        int i
    
    if n <= 0:
        return []
    
    for i in range(n):
        Py_INCREF(current)  
        PyList_SET_ITEM(dates, i, current)
        current += step
    
    return dates


cpdef cnp.ndarray[cnp.int64_t] timestamp_s_range(datetime start, datetime end, timedelta step):
    cdef:
        int64_t start_ts = <int64_t>floor(start.timestamp())
        int64_t end_ts = <int64_t>floor(end.timestamp())
        int64_t step_sec = <int64_t>step.total_seconds()
        int64_t n = (end_ts - start_ts) // step_sec + 1
        cnp.ndarray[cnp.int64_t] timestamps = np.empty(n, dtype=np.int64)
        int64_t i
    
    if n <= 0:
        return np.array([], dtype=np.int64)
    
    with nogil: 
        for i in prange(n, schedule='static'):
            timestamps[i] = start_ts + i * step_sec
    
    return timestamps

cpdef list timestamp_str_range(datetime start, datetime end, timedelta step, str format="%Y-%m-%d %H:%M:%S"):
    """
    Returns a list of timestamp strings in the specified format.
    
    Args:
        start: Start datetime
        end: End datetime
        step: Time step
        format: String format for timestamps (default: "%Y-%m-%d %H:%M:%S")
    
    Returns:
        List of formatted timestamp strings
    """
    current = start
    result = []
    while current <= end:
        result.append(current.strftime(format))
        current += step
    return result


