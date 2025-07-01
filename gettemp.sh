#!/bin/bash

set -ex

cd /home/bresnaha/Dev/pooltemperature
. venv/bin/activate

python3 pool.py >> /home/bresnaha/Dev/pooltemperature/data.csv
