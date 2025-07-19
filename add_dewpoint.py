import numpy as np
import pandas as pd


def dew_point(temp_f, rh):
    temp_f = np.array(temp_f)
    rh = np.array(rh)

    # Treat 0 or NaN as invalid
    valid = (temp_f != 0) & (rh != 0) & ~np.isnan(temp_f) & ~np.isnan(rh)

    dp = np.full_like(temp_f, fill_value=np.nan, dtype=np.float64)

    # Convert valid temps to Celsius
    temp_c = (temp_f[valid] - 32) * 5 / 9

    # Magnus formula constants
    a = 17.625
    b = 243.04
    alpha = (a * temp_c) / (b + temp_c) + np.log(rh[valid] / 100.0)
    dp_c = (b * alpha) / (a - alpha)

    # Convert back to Fahrenheit
    dp[valid] = dp_c * 9 / 5 + 32

    return dp


def add_dewpoint(df):
    df["dew_point"] = dew_point(df["outdoor"], df["humidity"])
    df.to_csv("output.csv", index=False)


def main():
    df = pd.read_csv("data.csv")
    add_dewpoint(df)


if __name__ == '__main__':
    main()
