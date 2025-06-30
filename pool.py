#!/usr/bin/env python

import logging
import os
import glob
import time
import datetime
import statistics


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def normalized_temperature_reading(device, reading_count=8, decimals=1):
    temp_list = []

    while len(temp_list) < reading_count:
        with open(device, "r") as f:
            lines = f.readlines()
        while lines[0].strip()[-3:] != "YES":
            time.sleep(0.2)
        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp = round(float(temp_string) / 1000.0, decimals)
            temp = float(temp_string) / 1000.0
            far = (temp * 1.8) + 32
            temp_list.append(far)
            logging.info(f"temp {far}")
            time.sleep(.5)

    mean = statistics.mean(temp_list)
    stddev = statistics.stdev(temp_list)

    logging.info(f"{temp_list} {mean} {stddev}")
    # Filter values within 1 standard deviation
    filtered = [x for x in temp_list if abs(x - mean) <= stddev]

    if not filtered:
        return float('nan')

    return statistics.mean(temp_list)


def read_temp(decimals=1, sleeptime=10):

    """Reads the temperature from a 1-wire device"""

    device = glob.glob("/sys/bus/w1/devices/" + "28*")[0] + "/w1_slave"
    while True:
        try:
            timepoint = datetime.datetime.now()
            timepassed = (datetime.datetime.now() - timepoint).total_seconds()
            equals_pos = lines[1].find("t=")
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp = round(float(temp_string) / 1000.0, decimals)

                int_seconds = int(time.time())
                far = round((temp * 1.8) + 32, decimals)
                print(f"{int_seconds} {far}")
                time.sleep(sleeptime-timepassed)
                timepoint = datetime.datetime.now()
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    device = glob.glob("/sys/bus/w1/devices/" + "28*")[0] + "/w1_slave"
    v = normalized_temperature_reading(device)
    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"{now_iso}, {v}")

