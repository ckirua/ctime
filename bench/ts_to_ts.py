import timeit

from ctime.conversions import change_ts_units


def raw_change_units(timestamp, from_unit, to_unit):
    """Pure Python implementation for comparison"""
    factors = {"ns": 1, "us": 1000, "ms": 1000000, "s": 1000000000}

    if from_unit == to_unit:
        return timestamp

    # Convert to nanoseconds first
    try:
        ns = timestamp * factors[from_unit]
    except KeyError:
        raise ValueError(f"Unsupported from_unit: {from_unit}")

    # Convert to target unit
    try:
        return ns // factors[to_unit]
    except KeyError:
        raise ValueError(f"Unsupported to_unit: {to_unit}")


def benchmark():
    """Benchmark Cython vs Python implementations"""
    units = ["ns", "us", "ms", "s"]
    test_values = {"ns": 1_000_000_000, "us": 1_000_000, "ms": 1_000, "s": 1}

    results = []
    for from_unit in units:
        for to_unit in units:
            val = test_values[from_unit]

            # Benchmark Cython implementation
            cython_time = timeit.timeit(
                lambda: change_ts_units(val, from_unit, to_unit), number=100_000
            )

            # Benchmark Python implementation
            python_time = timeit.timeit(
                lambda: raw_change_units(val, from_unit, to_unit),
                number=100_000,
            )

            results.append(
                (
                    f"{from_unit}->{to_unit}",
                    cython_time,
                    python_time,
                    python_time / cython_time,
                )
            )

    # Print results
    print(
        f"{'Conversion':<10} | {'Cython (ms)':>10} | {'Python (ms)':>10} | {'Speedup':>10}"
    )
    print("-" * 55)
    for res in results:
        print(
            f"{res[0]:<10} | {res[1]*1000:>10.4f} | {res[2]*1000:>10.4f} | {res[3]:>10.1f}x"
        )


if __name__ == "__main__":
    benchmark()
