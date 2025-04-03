from datetime import datetime, timedelta

from ctime import timestamp_str_range

if __name__ == "__main__":
    # Create a range of timestamp strings
    start = datetime(2023, 1, 1)
    end = datetime(2023, 1, 5)
    step = timedelta(days=1)
    format_str = "%Y-%m-%d"

    # Generate the timestamp strings
    timestamps = timestamp_str_range(start, end, step, format_str)

    # Print the results
    print("Generated timestamp strings:")
    for ts in timestamps:
        print(ts)

    # Example output:
    # Generated timestamp strings:
    # 2023-01-01
    # 2023-01-02
    # 2023-01-03
    # 2023-01-04
