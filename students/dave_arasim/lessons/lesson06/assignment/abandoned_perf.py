"""
better performing, better written module
"""

import datetime
import csv


def analyze(filename):
    start = datetime.datetime.now()

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        found = 0

        # Use dictionary as an emulated 'switch' statement for year tally
        year_function_dict = {
            2013: incr_2013,
            2014: incr_2014,
            2015: incr_2015,
            2016: incr_2016,
            2017: incr_2017,
            2018: incr_2018
        }

        # Dictionary to tally years in range 2013 - 2018
        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        for row in reader:
            try:
                this_year = int(row[5][6:])
            except ValueError:
                this_year = 0
            else:
                try:
                    year_function_dict.get(this_year)(year_count)
                except TypeError:
                    this_year = 0

            if 'ao' in row[6]:
                found += 1

        print(year_count)
        print(f"'ao' was found {found} times")

        end = datetime.datetime.now()

    return (start, end, year_count, found)


def incr_2013(year_count):
    year_count["2013"] += 1


def incr_2014(year_count):
    year_count["2014"] += 1


def incr_2015(year_count):
    year_count["2015"] += 1


def incr_2016(year_count):
    year_count["2016"] += 1


def incr_2017(year_count):
    year_count["2017"] += 1


def incr_2018(year_count):
    year_count["2018"] += 1


def main():
    filename = "exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
