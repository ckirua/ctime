import statistics
import time
from datetime import datetime, timedelta

from ctime import (
    get_daily_date_range,
    get_daily_timestamps,
    get_daily_timestamps_vectorized,
)


def python_date_range(
    start_date: datetime,
    end_date: datetime,
    delta: timedelta = timedelta(days=1),
) -> list[datetime]:
    days_diff = (end_date - start_date).days + 1
    return [start_date + delta * i for i in range(days_diff)]


def python_timestamps_range(
    start_date: datetime,
    end_date: datetime,
    delta: timedelta = timedelta(days=1),
) -> list[float]:
    days_diff = (end_date - start_date).days + 1
    return [(start_date + delta * i).timestamp() for i in range(days_diff)]


def benchmark_date_range(
    func,
    start_date: datetime,
    end_date: datetime,
    delta: timedelta = timedelta(days=1),
    iterations: int = 100,
):
    times = []
    result = None

    # Warm-up run
    func(start_date, end_date, delta)

    for _ in range(iterations):
        start_time = time.perf_counter()
        result = func(start_date, end_date, delta)
        end_time = time.perf_counter()
        times.append(end_time - start_time)

    # Return median time to reduce impact of outliers
    return statistics.median(times), len(result)


def main():
    # Test cases with different date ranges
    test_cases = [
        ("1 week", datetime(2024, 1, 1), datetime(2024, 1, 7)),
        ("1 month", datetime(2024, 1, 1), datetime(2024, 1, 31)),
        ("1 year", datetime(2024, 1, 1), datetime(2024, 12, 31)),
        ("10 years", datetime(2020, 1, 1), datetime(2029, 12, 31)),
    ]

    # Different intervals to test
    intervals = [
        ("daily", timedelta(days=1)),
        ("weekly", timedelta(weeks=1)),
        ("monthly", timedelta(days=30)),
    ]

    print("\nDate Range Benchmark Results:")
    print("-" * 80)
    print(
        f"{'Test Case':<15} {'Interval':<10} {'Python (s)':<12} {'Cython (s)':<12} {'Timestamps (s)':<15} {'TS Vec (s)':<15} {'Speedup':<10} {'TS Speedup':<12} {'TS Vec Speedup':<15} {'Count':<10}"
    )
    print("-" * 80)

    for case_name, start, end in test_cases:
        for interval_name, interval in intervals:
            # Run Python implementation
            py_time, py_count = benchmark_date_range(
                python_date_range, start, end, interval
            )

            # Run Cython implementation
            cy_time, cy_count = benchmark_date_range(
                get_daily_date_range, start, end, interval
            )

            # Run timestamps implementation
            ts_time, ts_count = benchmark_date_range(
                get_daily_timestamps, start, end, interval
            )

            # Run vectorized timestamps implementation
            ts_vec_time, ts_vec_count = benchmark_date_range(
                get_daily_timestamps_vectorized, start, end, interval
            )

            # Calculate speedup
            speedup = py_time / cy_time if cy_time > 0 else float("inf")
            ts_speedup = py_time / ts_time if ts_time > 0 else float("inf")
            ts_vec_speedup = (
                py_time / ts_vec_time if ts_vec_time > 0 else float("inf")
            )

            print(
                f"{case_name:<15} {interval_name:<10} {py_time:>11.6f} {cy_time:>11.6f} {ts_time:>14.6f} {ts_vec_time:>14.6f} {speedup:>9.2f}x {ts_speedup:>11.2f}x {ts_vec_speedup:>14.2f}x {py_count:>9}"
            )


if __name__ == "__main__":
    main()
