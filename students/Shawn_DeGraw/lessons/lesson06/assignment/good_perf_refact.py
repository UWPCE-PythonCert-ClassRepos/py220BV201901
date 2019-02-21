"""
Analyze module with performance improvements

"""

import datetime

def analyze(filename):
    """ Analyze the file for specific data """

    start = datetime.datetime.now()
    found = 0

    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }

    with open(filename) as csvfile:

        for line in csvfile:
            lrow = list(line.strip().split(','))

            if "ao" in lrow[6]:
                found += 1

            if lrow[5] > '00/00/2012':
                try:
                    year_count[
                        (lambda x: lrow[5][6:] if lrow[5][6:] != '2018' else '2017')(lrow)
                        ] += 1
                except KeyError:
                    continue

        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)


def main():
    """ Main to call function """

    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()