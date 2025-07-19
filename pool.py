#!/usr/bin/env python

import logging
import glob
import time
import datetime
import statistics
import adafruit_dht
import board

import numpy as np


dht_device = adafruit_dht.DHT22(board.D17)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


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


def normalize_list(temp_list):
    mean = statistics.mean(temp_list)
    if len(temp_list) < 5:
        return mean
    stddev = statistics.stdev(temp_list)

    logging.info(f"{temp_list} {mean} {stddev}")
    filtered = [x for x in temp_list if abs(x - mean) <= stddev]
    if not filtered:
        return float('nan')

    return statistics.mean(temp_list)


def get_pool_temp(reading_count=5):
    device = glob.glob("/sys/bus/w1/devices/" + "28*")[0] + "/w1_slave"

    temp_list = []

    while len(temp_list) < reading_count:
        with open(device, "r") as f:
            lines = f.readlines()
        while lines[0].strip()[-3:] != "YES":
            time.sleep(0.2)
        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp = float(temp_string) / 1000.0
            far = (temp * 1.8) + 32
            temp_list.append(far)
            logging.info(f"temp {far}")
            time.sleep(3)

    return normalize_list(temp_list)


def get_outdoor_temp(reading_count=12):
    temp_list = []
    humidity_list = []
    error = 0

    while len(temp_list) < reading_count:
        try:
            temperature_c = dht_device.temperature
            temperature_f = temperature_c * (9 / 5) + 32

            temp_list.append(temperature_f)

            humidity = dht_device.humidity
            humidity_list.append(humidity)

            logging.info("Temp:{:.1f} C / {:.1f} F  Humidity: {}%".format(temperature_c, temperature_f, humidity))
            time.sleep(5)
        except Exception as err:
            logging.error(err.args[0])
            error = error + 1
            if error > 5:
                return None, None
            time.sleep(3)

    return normalize_list(temp_list), normalize_list(humidity_list)


if __name__ == "__main__":
    v = get_pool_temp()
    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    ot, oh = get_outdoor_temp()
    if ot is None or oh is None:
        print(f"{now_iso}, {v}")
    else:
        dp = dew_point(ot, oh)
        print(f"{now_iso}, {v}, {ot}, {oh}, {dp}")


