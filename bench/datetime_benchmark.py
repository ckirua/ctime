import timeit
from datetime import datetime, timedelta

# Import the compiled Cython module
from ctime import date_range_cython, date_range_numeric


def run_benchmark():
    # Setup test parameters
    start = datetime(2023, 1, 1)
    end = datetime(2026, 12, 31)  # 4 years of daily dates
    step = timedelta(days=1)
    expected_count = 4 * 365 + 1  # +1 for leap year in 2024
    iterations = 10000  # Number of iterations for timeit

    # Warm-up runs (not timed)
    for _ in range(3):
        date_range_cython(start, end, step)
        date_range_numeric(start, end, step)

    # Test the Cython method
    test_func_cython = lambda: date_range_cython(start, end, step)
    test_func_numeric = lambda: date_range_numeric(start, end, step)

    # Run timeit with the specified number of iterations
    total_time_cython = timeit.timeit(test_func_cython, number=iterations)
    total_time_numeric = timeit.timeit(test_func_numeric, number=iterations)

    # Calculate average time per iteration
    avg_time_cython = total_time_cython / iterations
    avg_time_numeric = total_time_numeric / iterations

    # Verify correctness (run once outside timing)
    result_cython = date_range_cython(start, end, step)
    result_numeric = date_range_numeric(start, end, step)

    assert len(result_cython) == expected_count
    assert result_cython[0] == start
    assert result_cython[-1] == end

    assert len(result_numeric) == expected_count
    assert result_numeric[0] == int(start.timestamp())
    assert result_numeric[-1] == int(end.timestamp())

    # Print results
    print("\nDate Range Generation Benchmark (365 days)")
    print(f"Number of iterations: {iterations}")
    print("-" * 50)
    print(f"{'Method':<15} | {'Avg Time (ms)':<12}")
    print("-" * 50)
    time_ms_cython = avg_time_cython * 1000
    time_ms_numeric = avg_time_numeric * 1000
    print(f"{'Cython':<15} | {time_ms_cython:>11.3f}")
    print(f"{'Numeric':<15} | {time_ms_numeric:>11.3f}")


if __name__ == "__main__":
    run_benchmark()
