import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta


# Load the data

def make_graph():
    df = pd.read_csv("data.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%dT%H:%M:%SZ", utc=True)

    df["timestamp"] = df["timestamp"].dt.tz_convert("America/Chicago")

    latest_day = df["timestamp"].max().normalize()
    start_day = latest_day - timedelta(days=4)

    mask = (df["timestamp"] >= start_day) & (df["timestamp"] < latest_day + timedelta(days=1))
    df_filtered = df[mask]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df_filtered["timestamp"], df_filtered["temperature"], marker='o', linestyle='-')

    ax.set_ylim(50, 100)

    ax.set_xlim(start_day, latest_day + timedelta(days=1))

    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%a %m-%d', tz=df_filtered["timestamp"].dt.tz))

    ax.set_title("Temperature Over the Last 5 Days")
    ax.set_xlabel("Date (Chicago Time)")
    ax.set_ylabel("Temperature (°F)")
    plt.xticks(rotation=45)
    ax.grid(True)

    plt.tight_layout()
    plt.savefig("temperature_plot.png", dpi=300)


def main():
    make_graph()


if __name__ == '__main__':
    main()
