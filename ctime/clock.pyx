from posix.time cimport timespec, clock_gettime, CLOCK_MONOTONIC_RAW, CLOCK_MONOTONIC, CLOCK_REALTIME, CLOCK_MONOTONIC_COARSE, CLOCK_REALTIME_COARSE
from libc.stdint cimport uint64_t


cpdef inline uint64_t clock_monotonic_raw() noexcept nogil:
    cdef timespec ts
    clock_gettime(CLOCK_MONOTONIC_RAW, &ts)
    return (<uint64_t>ts.tv_sec * 1000000000) + <uint64_t>ts.tv_nsec


cpdef inline uint64_t clock_monotonic() noexcept nogil:
    cdef timespec ts
    clock_gettime(CLOCK_MONOTONIC, &ts)
    return (<uint64_t>ts.tv_sec * 1000000000) + <uint64_t>ts.tv_nsec


cpdef inline uint64_t clock_realtime() noexcept nogil:
    cdef timespec ts
    clock_gettime(CLOCK_REALTIME, &ts)
    return (<uint64_t>ts.tv_sec * 1000000000) + <uint64_t>ts.tv_nsec


cpdef inline uint64_t clock_monotonic_coarse() noexcept nogil:
    cdef timespec ts
    clock_gettime(CLOCK_MONOTONIC_COARSE, &ts)
    return (<uint64_t>ts.tv_sec * 1000000000) + <uint64_t>ts.tv_nsec


cpdef inline uint64_t clock_realtime_coarse() noexcept nogil:
    cdef timespec ts
    clock_gettime(CLOCK_REALTIME_COARSE, &ts)
    return (<uint64_t>ts.tv_sec * 1000000000) + <uint64_t>ts.tv_nsec
