cimport cython
cimport numpy as np
from cpython cimport PyObject, PyTypeObject
from cpython.datetime cimport PyDateTime_IMPORT, datetime
from libc.stdint cimport int64_t
import numpy as np


# Import datetime C API
PyDateTime_IMPORT 
cdef extern from "datetime.h":
    ctypedef struct PyDateTime_CAPI:
        PyTypeObject *DateTimeType
        PyObject *TimeZone_UTC
        PyObject *(*DateTime_FromTimestamp)(PyObject*, PyObject*, PyObject*)
    
    PyDateTime_CAPI *PyDateTimeAPI

# Enum ?
cdef:
    int64_t NS_PER_US = 1000
    int64_t NS_PER_MS = 1000000
    int64_t NS_PER_SECOND = 1000000000
    int64_t US_PER_SECOND = 1000000
    int64_t MS_PER_SECOND = 1000
    int64_t SECONDS_PER_DAY = 86400
    # Unix epoch (1970-01-01) as datetime64[ns] for reference
    int64_t UNIX_EPOCH_NS = 0

cdef inline object ns_to_datetime_fast(int64_t ns_timestamp):
    cdef double seconds = ns_timestamp / <double>NS_PER_SECOND
    cdef tuple args = (seconds, <object>PyDateTimeAPI.TimeZone_UTC)
    cdef PyObject* result = PyDateTimeAPI.DateTime_FromTimestamp(
        <PyObject*>PyDateTimeAPI.DateTimeType,
        <PyObject*>args,
        NULL
    )
    if result == NULL:
        raise RuntimeError("Failed to create datetime from timestamp")
    return <object>result

cdef inline object us_to_datetime_fast(int64_t us_timestamp):
    cdef double seconds = us_timestamp / <double>US_PER_SECOND
    cdef tuple args = (seconds, <object>PyDateTimeAPI.TimeZone_UTC)
    cdef PyObject* result = PyDateTimeAPI.DateTime_FromTimestamp(
        <PyObject*>PyDateTimeAPI.DateTimeType,
        <PyObject*>args,
        NULL
    )
    if result == NULL:
        raise RuntimeError("Failed to create datetime from timestamp")
    return <object>result

cdef inline object ms_to_datetime_fast(int64_t ms_timestamp):
    cdef double seconds = ms_timestamp / <double>MS_PER_SECOND
    cdef tuple args = (seconds, <object>PyDateTimeAPI.TimeZone_UTC)
    cdef PyObject* result = PyDateTimeAPI.DateTime_FromTimestamp(
        <PyObject*>PyDateTimeAPI.DateTimeType,
        <PyObject*>args,
        NULL
    )
    if result == NULL:
        raise RuntimeError("Failed to create datetime from timestamp")
    return <object>result

cdef inline object s_to_datetime_fast(int64_t s_timestamp):
    cdef double seconds = <double>s_timestamp
    cdef tuple args = (seconds, <object>PyDateTimeAPI.TimeZone_UTC)
    cdef PyObject* result = PyDateTimeAPI.DateTime_FromTimestamp(
        <PyObject*>PyDateTimeAPI.DateTimeType,
        <PyObject*>args,
        NULL
    )
    if result == NULL:
        raise RuntimeError("Failed to create datetime from timestamp")
    return <object>result

cpdef datetime ns_to_datetime(int64_t ns_timestamp):
    """
    Convert nanoseconds since Unix epoch to Python datetime.
    """
    return ns_to_datetime_fast(ns_timestamp)

cpdef datetime us_to_datetime(int64_t us_timestamp):
    """
    Convert microseconds since Unix epoch to Python datetime.
    """
    return us_to_datetime_fast(us_timestamp)

cpdef datetime ms_to_datetime(int64_t ms_timestamp):
    """
    Convert milliseconds since Unix epoch to Python datetime.
    """
    return ms_to_datetime_fast(ms_timestamp)

cpdef datetime s_to_datetime(int64_t s_timestamp):
    """
    Convert seconds since Unix epoch to Python datetime.
    """
    return s_to_datetime_fast(s_timestamp)

def datetime_to_ns(dt):
    """
    Convert Python datetime to nanoseconds since Unix epoch.
    """
    cdef:
        int64_t ns
    ns = <int64_t>(dt.timestamp() * NS_PER_SECOND)
    return ns

def datetime_to_us(dt):
    """
    Convert Python datetime to microseconds since Unix epoch.
    """
    cdef:
        int64_t us
    us = <int64_t>(dt.timestamp() * US_PER_SECOND)
    return us

def datetime_to_ms(dt):
    """
    Convert Python datetime to milliseconds since Unix epoch.
    """
    cdef:
        int64_t ms
    ms = <int64_t>(dt.timestamp() * MS_PER_SECOND)
    return ms

def datetime_to_s(dt):
    """
    Convert Python datetime to seconds since Unix epoch.
    """
    return dt.timestamp()

@cython.boundscheck(False)
@cython.wraparound(False)
def ns_array_to_datetime(np.ndarray[int64_t] ns_array):
    """
    Convert numpy array of nanosecond timestamps to array of datetime objects.
    Optimized for bulk conversions.
    """
    cdef:
        Py_ssize_t i, n = ns_array.shape[0]
        np.ndarray[object] out = np.empty(n, dtype=object)
        int64_t ns
    
    for i in range(n):
        ns = ns_array[i]
        out[i] = datetime.utcfromtimestamp(ns / <double>NS_PER_SECOND)
    
    return out

@cython.boundscheck(False)
@cython.wraparound(False)
def datetime_array_to_ns(np.ndarray[object] dt_array):
    """
    Convert numpy array of datetime objects to array of nanosecond timestamps.
    Optimized for bulk conversions.
    """
    cdef:
        Py_ssize_t i, n = dt_array.shape[0]
        np.ndarray[int64_t] out = np.empty(n, dtype='int64')
        object dt
    
    for i in range(n):
        dt = dt_array[i]
        out[i] = <int64_t>(dt.timestamp() * NS_PER_SECOND)
    
    return out

def adjust_timestamp(int64_t timestamp, str from_unit='ns', str to_unit='ns'):
    """
    Convert between different time units.
    Supported units: 'ns', 'us', 'ms', 's'
    """
    cdef:
        int64_t factor
    
    if from_unit == to_unit:
        return timestamp
    
    # Convert to nanoseconds first
    if from_unit == 'us':
        timestamp *= NS_PER_US
    elif from_unit == 'ms':
        timestamp *= NS_PER_MS
    elif from_unit == 's':
        timestamp *= NS_PER_SECOND
    elif from_unit != 'ns':
        raise ValueError(f"Unsupported from_unit: {from_unit}")
    
    # Convert from nanoseconds to target unit
    if to_unit == 'us':
        return timestamp // NS_PER_US
    elif to_unit == 'ms':
        return timestamp // NS_PER_MS
    elif to_unit == 's':
        return timestamp // NS_PER_SECOND
    elif to_unit == 'ns':
        return timestamp
    else:
        raise ValueError(f"Unsupported to_unit: {to_unit}")