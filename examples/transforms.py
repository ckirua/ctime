from datetime import datetime, timedelta

import numpy as np
from ctime import (
    adjust_timestamp,
    datetime_array_to_ns,
    datetime_to_ms,
    datetime_to_ns,
    datetime_to_s,
    datetime_to_us,
    ms_to_datetime,
    ns_to_datetime,
    s_to_datetime,
    us_to_datetime,
)

if __name__ == "__main__":
    # Create a sample datetime
    dt = datetime(2023, 1, 1, 12, 0, 0)

    # Convert datetime to different units
    print("Datetime conversions:")
    print(f"Original datetime: {dt}")
    print(f"To nanoseconds: {datetime_to_ns(dt)}")
    print(f"To microseconds: {datetime_to_us(dt)}")
    print(f"To milliseconds: {datetime_to_ms(dt)}")
    print(f"To seconds: {datetime_to_s(dt)}")

    # Convert from different units back to datetime
    ns = datetime_to_ns(dt)
    us = datetime_to_us(dt)
    ms = datetime_to_ms(dt)
    s = datetime_to_s(dt)

    print("\nUnit conversions back to datetime:")
    print(f"From nanoseconds: {ns_to_datetime(ns)}")
    print(f"From microseconds: {us_to_datetime(us)}")
    print(f"From milliseconds: {ms_to_datetime(ms)}")
    print(f"From seconds: {s_to_datetime(s)}")

    # Array conversions
    print("\nArray conversions:")
    dt_array = np.array(
        [dt, dt + timedelta(days=1), dt + timedelta(days=2)], dtype=object
    )
    ns_array = datetime_array_to_ns(dt_array)
    print(f"Datetime array to nanoseconds: {ns_array}")

    # Commenting out the line that causes segmentation fault
    # print(f"Nanoseconds array back to datetime: {ns_array_to_datetime(ns_array)}")

    # Unit adjustment
    print("\nUnit adjustments:")
    print(
        f"1 second in nanoseconds: {adjust_timestamp(1, from_unit='s', to_unit='ns')}"
    )
    print(
        f"1000 milliseconds in seconds: {adjust_timestamp(1000, from_unit='ms', to_unit='s')}"
    )
    print(
        f"5000000 microseconds in milliseconds: {adjust_timestamp(5000000, from_unit='us', to_unit='ms')}"
    )
