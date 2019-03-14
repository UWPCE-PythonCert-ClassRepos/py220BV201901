"""
Yushu Song
Assignment 06

"""

import csv
import datetime

def analyze(filename):
    start = datetime.datetime.now()
    with open(filename, encoding='ascii') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        BASE_YEAR = 2013
        year_count = [0] * 6

        found = 0
        for row in reader:
            lrow = list(row)
            if lrow[5] > '00/00/2012':
                i = int(lrow[5][6:]) - BASE_YEAR
                if i >= 0 and i < 6:
                    year_count[i] += 1
            if "ao" in lrow[6]:
                found += 1

        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    year_count = {str(i + BASE_YEAR): v for i, v in enumerate(year_count)}
    print(year_count)
    return (start, end, year_count, found)

def main():
    filename = "data/exercise.csv"
    result = analyze(filename)
    print(f"Time spent: {result[1]-result[0]}")

if __name__ == "__main__":
    main()
