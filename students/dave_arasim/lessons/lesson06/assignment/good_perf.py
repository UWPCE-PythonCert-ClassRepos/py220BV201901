"""
good performing, good written module
"""

import datetime
import csv

def analyze(filename):
    start = datetime.datetime.now()

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        found = 0

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        for row in reader:
            this_year = row[5][6:]

            if (this_year > '2012') and (this_year < '2019'):
                if this_year == '2013':
                    year_count["2013"] += 1
                elif this_year == '2014':
                    year_count["2014"] += 1
                elif this_year == '2015':
                    year_count["2015"] += 1
                elif this_year == '2016':
                    year_count["2016"] += 1
                elif this_year == '2017':
                    year_count["2017"] += 1
                elif this_year == '2018':
                    year_count["2018"] += 1

            if 'ao' in row[6]:
                found += 1

        print(year_count)
        print(f"'ao' was found {found} times")

        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    filename = "exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
