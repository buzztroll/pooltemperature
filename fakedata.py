
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuration
start_time = datetime(2025, 5, 1, 0, 0, 0)
datapoints = 500 # Two days of data

# Generate timestamps (every hour)
timestamps = [start_time + timedelta(hours=i*4) for i in range(datapoints)]

# Generate fake temperature data with slight variation
# Base around 65–85°F daytime temps
temperatures = []
for t in timestamps:
    hour = t.hour
    # Simulate daytime warmth and nighttime cool
    base_temp = 85 if 11 <= hour <= 17 else 65
    temp = base_temp + np.random.normal(0, 2)  # add noise
    temperatures.append(round(temp, 1))

# Build DataFrame
df = pd.DataFrame({
    "timestamp": [ts.isoformat() + "Z" for ts in timestamps],  # UTC ISO format
    "temperature": temperatures
})

# Save to CSV
df.to_csv("fake_temperature_data.csv", index=False)

# Preview first few rows
print(df.tail())
