from cpython.list cimport PyList_New, PyList_SET_ITEM
from cpython.datetime cimport datetime, timedelta, PyDateTime_FromTimestamp
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def get_datetime_range(
    datetime start_date,
    datetime end_date,
    timedelta delta=None
):
    """Generate datetime objects with Cython optimizations"""
    if delta is None:
        delta = timedelta(days=1)
    
    cdef:
        double start_ts = datetime.timestamp(start_date)
        double delta_sec = delta.total_seconds()
        double end_ts = datetime.timestamp(end_date)
        int n = <int>((end_ts - start_ts) / delta_sec) + 1
        list result = PyList_New(n)
        int i
        double current_ts
        object py_dt
    
    for i in range(n):
        current_ts = start_ts + i * delta_sec
        py_dt = PyDateTime_FromTimestamp(current_ts)
        if start_date.tzinfo is not None:
            py_dt = py_dt.replace(tzinfo=start_date.tzinfo)
        PyList_SET_ITEM(result, i, py_dt)
    
    return result