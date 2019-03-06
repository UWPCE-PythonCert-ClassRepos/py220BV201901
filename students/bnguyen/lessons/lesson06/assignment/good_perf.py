# Student: Bradnon Nguyen
# Class:   Advance Python 220 - Jan2019
# Lesson06 - Profiling/Optimization.

"""
This module is used to show the improvement from poor_perf.py.
"""

import datetime
import csv


# @profile
def analyze(filename):
    """
    This function annalyze the data in a csv add update the count in each year.
    """
    start = datetime.datetime.now()

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # In the line_profiler we can see big hit and % time in this loop
        new_ones = []
        # new_ones = [(row[5], row[0]) for row in reader if row[5] > '00/00/2012']
        found = 0

        for row in reader:
            # lrow = list(line) # added time for nothing
            if row[5] > '00/00/2012':
                new_ones.append((row[5], row[0]))
            if "ao" in row[6]:
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
    """This is main."""
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
