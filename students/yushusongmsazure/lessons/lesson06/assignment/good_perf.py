"""
Yushu Song
Assignment 06

"""

import csv
import datetime
import logging
from functools import wraps

LOGGER = logging.getLogger()
# create file handler
FILE_HANDLER = logging.FileHandler('good_perf.log')
# create console handler
CONSOLE_HANDLER = logging.StreamHandler()
# create formatter
FORMATTER = logging.Formatter('%(asctime)s %(name)-6s %(levelname)-6s %(message)s')
# set formater to file handler
FILE_HANDLER.setFormatter(FORMATTER)
# set formater to console handler
CONSOLE_HANDLER.setFormatter(FORMATTER)
# add file handle
LOGGER.addHandler(FILE_HANDLER)
# add console handle
LOGGER.addHandler(CONSOLE_HANDLER)
# add log level at root level
LOGGER.setLevel(logging.INFO)


def profile(func):
    '''
    Profile how long a give function runs
    '''
    @wraps(func)
    def log_time(*args, **kwargs):
        start = datetime.datetime.now()
        x = func(*args, **kwargs)
        elapsed = datetime.datetime.now()
        LOGGER.info(f"[{func.__name__}] Elapsed Time = {elapsed-start}")
        return x
    return log_time

@profile
def analyze(filename):
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        found = 0
        for row in reader:
            lrow = list(row)
            if lrow[5] > '00/00/2012':
                new_ones.append((lrow[5], lrow[0]))
            if "ao" in lrow[6]:
                found += 1

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        for new in new_ones:
            if new[0][6:] == '2013':
                year_count["2013"] += 1
            if new[0][6:] == '2014':
                year_count["2014"] += 1
            if new[0][6:] == '2015':
                year_count["2015"] += 1
            if new[0][6:] == '2016':
                year_count["2016"] += 1
            if new[0][6:] == '2017':
                year_count["2017"] += 1
            if new[0][6:] == '2018':
                year_count["2017"] += 1

        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    filename = "data/exercise.csv"
    analyze(filename)

if __name__ == "__main__":
    main()
