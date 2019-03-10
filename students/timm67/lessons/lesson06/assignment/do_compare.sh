#!/bin/sh
export PYTHONPATH=.
rm -f ./data/exercise-new.csv
python3 ./poor_perf.py
rm -f ./data/exercise-new.csv
python3 ./good_perf.py
