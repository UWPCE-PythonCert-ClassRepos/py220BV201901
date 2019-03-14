"""
well performing, efficiently written module
"""

import csv
import cProfile
import datetime
from collections import Counter


def analyze(filename):
    """ Analyzed a CSV file to test performance """
    start = datetime.datetime.now()
    year_start = datetime.datetime.now()
    found = 0
    year_list = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:

            if "ao" in row[6]:
                found += 1

            if row[5][6:] > "2012" and row[5][6:] < "2019":
                year_list.append(int(row[5][6:]))

        year_count = Counter(year_list)

    year_end = datetime.datetime.now()
    print(year_count)

    end = datetime.datetime.now()
    print(f"'ao' was found {found} times")
    print(f"Total year run time: {year_end - year_start}")
    return (start, end, year_count, found)


def main():
    """ Main function of module """
    filename = "data/exercise-new.csv"
    analyze(filename)

if __name__ == "__main__":
    PR = cProfile.Profile()
    PR.enable()
    MODULE_START = datetime.datetime.now()
    main()
    MODULE_END = datetime.datetime.now()
    print(f"Total module run time: {MODULE_END - MODULE_START}")
    PR.disable()
    PR.print_stats()
    