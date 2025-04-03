# cython: language_level=3
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION

from cpython.datetime cimport datetime, PyDateTime_IMPORT, PyTypeObject, PyObject
from libc.stdint cimport int64_t
import numpy as np
cimport numpy as np
import cython
from datetime import timezone

PyDateTime_IMPORT  # Ensure datetime C API is initialized

# Import datetime.h for direct access to C-level datetime functions
cdef extern from "datetime.h":
    # Define the datetime C API structure
    ctypedef struct PyDateTime_CAPI:
        # Type objects
        PyTypeObject *DateType
        PyTypeObject *DateTimeType
        PyTypeObject *TimeType
        PyTypeObject *DeltaType
        PyTypeObject *TZInfoType
        
        # Constructor functions
        void* (*DateTime_FromDateAndTime)(int, int, int, int, int, int, int, void*, void*)
        void* (*Date_FromDate)(int, int, int, void*)
        void* (*Time_FromTime)(int, int, int, int, void*, void*)
        void* (*Delta_FromDelta)(int, int, int, int, void*)
        
        # Timestamp constructors
        void* (*DateTime_FromTimestamp)(void*, void*, void*)
        void* (*Date_FromTimestamp)(void*, void*)
    # UTC timezone singleton
    PyObject *TimeZone_UTC


# Constants for time conversions
cdef:
    int64_t NS_PER_US = 1000
    int64_t NS_PER_MS = 1000000
    int64_t NS_PER_SECOND = 1000000000
    int64_t US_PER_SECOND = 1000000
    int64_t MS_PER_SECOND = 1000
    int64_t SECONDS_PER_DAY = 86400

# Unix epoch (1970-01-01) as datetime64[ns] for reference
cdef:
    int64_t UNIX_EPOCH_NS = 0


cpdef datetime ns_to_datetime(int64_t ns_timestamp):
    """
    Convert nanoseconds since Unix epoch to Python datetime.
    """
    cdef double seconds = ns_timestamp / NS_PER_SECOND  
    return datetime.fromtimestamp(seconds, timezone.utc)

cpdef datetime us_to_datetime(int64_t us_timestamp):
    """
    Convert microseconds since Unix epoch to Python datetime.
    """
    cdef double seconds = us_timestamp / <double>US_PER_SECOND
    return datetime.fromtimestamp(seconds, timezone.utc)

cpdef datetime ms_to_datetime(int64_t ms_timestamp):
    """
    Convert milliseconds since Unix epoch to Python datetime.
    """
    cdef double seconds = ms_timestamp / <double>MS_PER_SECOND
    return datetime.fromtimestamp(seconds, timezone.utc)

cpdef datetime s_to_datetime(double s_timestamp):
    """
    Convert seconds since Unix epoch to Python datetime.
    """
    return datetime.fromtimestamp(s_timestamp, timezone.utc)

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