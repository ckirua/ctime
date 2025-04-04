import timeit
from datetime import datetime

from ctime import datetime_to_ms, datetime_to_ns, datetime_to_s, datetime_to_us


# Raw Python implementations for comparison
def py_datetime_to_ns(dt):
    return int(dt.timestamp() * 1e9)


def py_datetime_to_us(dt):
    return int(dt.timestamp() * 1e6)


def py_datetime_to_ms(dt):
    return int(dt.timestamp() * 1e3)


def py_datetime_to_s(dt):
    return dt.timestamp()


def bench_single_dt_conversions():
    # Setup
    dt = datetime.now()
    num_iterations = 1000000

    # Benchmark Cython implementations
    ns_time = timeit.timeit(lambda: datetime_to_ns(dt), number=num_iterations)
    us_time = timeit.timeit(lambda: datetime_to_us(dt), number=num_iterations)
    ms_time = timeit.timeit(lambda: datetime_to_ms(dt), number=num_iterations)
    s_time = timeit.timeit(lambda: datetime_to_s(dt), number=num_iterations)

    # Benchmark Python implementations
    py_ns_time = timeit.timeit(
        lambda: py_datetime_to_ns(dt), number=num_iterations
    )
    py_us_time = timeit.timeit(
        lambda: py_datetime_to_us(dt), number=num_iterations
    )
    py_ms_time = timeit.timeit(
        lambda: py_datetime_to_ms(dt), number=num_iterations
    )
    py_s_time = timeit.timeit(
        lambda: py_datetime_to_s(dt), number=num_iterations
    )

    print("\nSingle datetime conversion benchmarks:")
    print(f"Cython datetime_to_ns: {ns_time:.6f} seconds")
    print(f"Python datetime_to_ns: {py_ns_time:.6f} seconds")
    print(f"\nCython datetime_to_us: {us_time:.6f} seconds")
    print(f"Python datetime_to_us: {py_us_time:.6f} seconds")
    print(f"\nCython datetime_to_ms: {ms_time:.6f} seconds")
    print(f"Python datetime_to_ms: {py_ms_time:.6f} seconds")
    print(f"\nCython datetime_to_s: {s_time:.6f} seconds")
    print(f"Python datetime_to_s: {py_s_time:.6f} seconds")


if __name__ == "__main__":
    bench_single_dt_conversions()
