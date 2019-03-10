"""
better performing, revised module

"""

import time
import csv

from zipfile import ZipFile

ZIP_FILENAME_DBG = './lessons/lesson06/assignment/data/data.zip'
ZIP_FILENAME = './data/data.zip'
CSV_FILENAME = 'exercise-new.csv'
EXTRACT_PATH_DBG = './lessons/lesson06/assignment/'
EXTRACT_PATH = './data'

def extract_csv(zip_filename, csv_filename, extract_path):
    """
    Extract .csv file from .zip file (req'd for github file size limits)
    """
    with ZipFile(zip_filename, 'r') as ziparchive:
        # extract csv file using EXTRACT_PATH
        ziparchive.extract(csv_filename, path=extract_path)


def analyze(filename):
    start = time.perf_counter()
    ao_found = 0
    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        for row in reader:
            lrow = list(row)
            if "ao" in lrow[6]:
                ao_found += 1
            if lrow[5] > '00/00/2012':
                new_ones.append((lrow[5], lrow[0]))

        for new in new_ones:
            if new[0][6:] == '2013':
                year_count["2013"] += 1
            elif new[0][6:] == '2014':
                year_count["2014"] += 1
            elif new[0][6:] == '2015':
                year_count["2015"] += 1
            elif new[0][6:] == '2016':
                year_count["2016"] += 1
            elif new[0][6:] == '2017':
                year_count["2017"] += 1
            elif new[0][6:] == '2018':
                year_count["2017"] += 1

    print(year_count)
    end = time.perf_counter()

    return (start, end, year_count, ao_found)


def main():
    print(f"Extracting [{EXTRACT_PATH}{CSV_FILENAME}] from [{ZIP_FILENAME}]")
    extract_csv(ZIP_FILENAME, CSV_FILENAME, EXTRACT_PATH)
    filename = "data/exercise-new.csv"
    ret = analyze(filename)
    print(f"start[{ret[0]}] end[{ret[1]}]")
    print(f"ao found [{ret[3]}] times")


if __name__ == "__main__":
    main()
