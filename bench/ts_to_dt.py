import timeit
from datetime import datetime, timezone

from ctime import ms_to_datetime, ns_to_datetime, s_to_datetime, us_to_datetime


def python_ns_to_datetime(ns_timestamp):
    """
    Pure Python implementation of ns_to_datetime
    """
    seconds = ns_timestamp / 1_000_000_000.0
    return datetime.fromtimestamp(seconds, timezone.utc)


def python_us_to_datetime(us_timestamp):
    """
    Pure Python implementation of us_to_datetime
    """
    seconds = us_timestamp / 1_000_000.0
    return datetime.fromtimestamp(seconds, timezone.utc)


def python_ms_to_datetime(ms_timestamp):
    """
    Pure Python implementation of ms_to_datetime
    """
    seconds = ms_timestamp / 1_000.0
    return datetime.fromtimestamp(seconds, timezone.utc)


def python_s_to_datetime(s_timestamp):
    """
    Pure Python implementation of s_to_datetime
    """
    return datetime.fromtimestamp(s_timestamp, timezone.utc)


def run_benchmark():
    # Test values
    ns_value = 1672567200000000000  # 2023-01-01 12:00:00
    us_value = 1672567200000000
    ms_value = 1672567200000
    s_value = 1672567200
    iterations = 1000000

    # Define test functions
    test_funcs = [
        ("ns_to_datetime (Cython)", lambda: ns_to_datetime(ns_value)),
        ("ns_to_datetime (Python)", lambda: python_ns_to_datetime(ns_value)),
        ("us_to_datetime (Cython)", lambda: us_to_datetime(us_value)),
        ("us_to_datetime (Python)", lambda: python_us_to_datetime(us_value)),
        ("ms_to_datetime (Cython)", lambda: ms_to_datetime(ms_value)),
        ("ms_to_datetime (Python)", lambda: python_ms_to_datetime(ms_value)),
        ("s_to_datetime (Cython)", lambda: s_to_datetime(s_value)),
        ("s_to_datetime (Python)", lambda: python_s_to_datetime(s_value)),
    ]

    # Warm-up runs
    for _, func in test_funcs:
        for _ in range(10):
            func()

    # Run benchmarks
    results = []
    for name, func in test_funcs:
        total_time = timeit.timeit(func, number=iterations)
        avg_time_ms = (total_time / iterations) * 1000
        results.append((name, avg_time_ms))

    # Print results
    print("\nTimestamp to Datetime Conversion Benchmark")
    print(f"Number of iterations: {iterations}")
    print("-" * 60)
    print(f"{'Function':<30} | {'Avg Time (μs)':<15}")
    print("-" * 60)

    for i in range(0, len(results), 2):
        cython_name, cython_time = results[i]
        python_name, python_time = results[i + 1]

        # Convert ms to μs for display
        cython_time_us = cython_time * 1000
        python_time_us = python_time * 1000
        speedup = python_time / cython_time

        print(f"{cython_name:<30} | {cython_time_us:>15.3f}")
        print(f"{python_name:<30} | {python_time_us:>15.3f}")
        print(f"Speedup: {speedup:.2f}x")
        print("-" * 60)


if __name__ == "__main__":
    run_benchmark()
