import sys
import logging

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


# Load the data

def make_graph(days_back=5):
    df = pd.read_csv("output.csv")

    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%dT%H:%M:%SZ", utc=True)

    df["timestamp"] = df["timestamp"].dt.tz_convert("America/Chicago")

    latest_day = df["timestamp"].max().normalize()
    start_day = latest_day - timedelta(days=days_back)

    mask = (df["timestamp"] >= start_day) & (df["timestamp"] < latest_day + timedelta(days=1))
    df_filtered = df[mask]

    fig, ax = plt.subplots(figsize=(10, 5))
    # Left Y-axis
    ax.plot(df_filtered["timestamp"], df_filtered["temperature"], label="pool", color="blue")
    ax.plot(df_filtered["timestamp"], df_filtered["outdoor"], label="outdoor", color="green")
    ax.plot(df_filtered["timestamp"], df_filtered["dewpoint"], label="dewpoint", color="red")
    ax.set_ylabel("Temperature (°F)")
    ax.set_ylim(60, 100)

    # Right Y-axis for humidity
    ax2 = ax.twinx()
    ax2.plot(df_filtered["timestamp"], df_filtered["humidity"], label="humidity", color="orange", linestyle="--")
    ax2.set_ylabel("Humidity (%)", color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')
    ax2.set_ylim(0, 100)

    interval = int((days_back * 24) / 10)
    # Time formatting
    ax.set_xlim(start_day, latest_day + timedelta(days=1))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=interval))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%a %m-%d : %H', tz=df_filtered["timestamp"].dt.tz))
    for label in ax.get_xticklabels():
        label.set_rotation(45)

    # Combined legend
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    ax.set_title(f"Temperature and Humidity Over the Last {days_back} Days")
    ax.set_xlabel("Date (Chicago Time)")
    ax.grid(True)
    plt.tight_layout()
    plt.savefig("temperature_plot.png", dpi=300)


def main(db):
    make_graph(db)


if __name__ == '__main__':
    try:
        db = int(sys.argv[1])
    except:
        db = 5
    main(db)
