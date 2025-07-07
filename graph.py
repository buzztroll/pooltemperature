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

    ax.plot(df_filtered["timestamp"], df_filtered["temperature"], label="pool", marker=',', linestyle='-', color='blue')
#    ax.plot(df_filtered["timestamp"], df_filtered["outdoor"], label="outdoor", marker='.', linestyle='-', color='green')

    ax.set_ylim(60, 95)

    ax.set_xlim(start_day, latest_day + timedelta(days=1))

    ax.xaxis.set_major_locator(mdates.HourLocator(interval=12))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%a %m-%d : %H', tz=df_filtered["timestamp"].dt.tz))

    ax.set_title("Temperature Over the Last 5 Days")
    ax.set_xlabel("Date (Chicago Time)")
    ax.set_ylabel("Temperature (°F)")

    # ax2 = ax.twinx()
    # ax2.plot(df_filtered["timestamp"], df_filtered["humidity"], label="humidity", linestyle='--', color='orange')
    # ax2.set_ylabel("Humidity (%)", color='orange')
    # ax2.tick_params(axis='y', labelcolor='orange')

    plt.xticks(rotation=45)
    ax.grid(True)

    plt.legend()
    plt.tight_layout()
    plt.savefig("temperature_plot.png", dpi=300)


def main():
    make_graph()


if __name__ == '__main__':
    main()
