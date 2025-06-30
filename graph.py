import datetime

import pandas as pd
import matplotlib.pyplot as plt

# Load the data

def make_graph(start_time, end_time):
    df = pd.read_csv("data.csv", parse_dates=["timestamp"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

    # Define your time range (replace with your actual range)
    # start_time = pd.Timestamp("2024-06-01T12:00:00Z")
    # end_time = pd.Timestamp("2025-06-01T14:00:00Z")
    #
    # Filter to that time range
    df_filtered = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]

    # Plot the filtered data
    plt.figure(figsize=(10, 5))
    plt.plot(df_filtered["timestamp"], df_filtered["temperature"], marker='o', linestyle='-')
    plt.ylim(bottom=40)

    # Formatting
    plt.title("Temperature Over Time (Filtered)")
    plt.xlabel("Time (UTC)")
    plt.ylabel("Temperature (°F)")
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)

    # Show the graph
    plt.savefig("temperature_plot.png", dpi=300)


def get_filter(start_str=None, end_str=None):
    time_now = pd.Timestamp.now(tz="America/Chicago")
    if start_str is None:
        start_time = time_now - pd.Timedelta(days=5)
    else:
        start_time = pd.to_datetime(start_str, format="%Y-%m-%d", errors="raise")
    if end_str is None:
        end_time = time_now
    else:
        end_time = pd.to_datetime(end_str, format="%Y-%m-%d", errors="raise")

    return start_time, end_time


def main():
    s, e = get_filter()
    make_graph(s, e)


if __name__ == '__main__':
    main()
