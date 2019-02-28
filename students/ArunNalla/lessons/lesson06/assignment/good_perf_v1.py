#! usr/bin/python3
"""
Lesson6 Assignment
Performane and profiling,
    Arun Nalla 02/26/2019
"""

import datetime
import csv

def analyze(filename):
    """ Extracting the year count and specfic line from single iterable list"""
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
            if 'ao' in row[6]:
                found += 1
            if row[5][6:] == '2013':
                year_count["2013"] += 1
            if row[5][6:] == '2014':
                year_count["2014"] += 1
            if row[5][6:] == '2015':
                year_count["2015"] += 1
            if row[5][6:] == '2016':
                year_count["2016"] += 1
            if row[5][6:] == '2017':
                year_count["2017"] += 1
            if row[5][6:] == '2018':
                year_count["2017"] += 1

        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()
    print(end-start, "Time taken to complete") # run time
    return (start, end, year_count, found)

def main():
    filename = "data/exercise.csv"
    analyze(filename)

if __name__ == "__main__":
    main()
