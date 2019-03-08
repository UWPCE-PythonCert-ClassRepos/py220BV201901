"""
improved the poor_perf.py
Used an evidence based approach to find out bottleneck
and implemented improvements.

"""

import datetime
import csv
import asyncio

def create_list_generator(filename):
    """
    this is a generator function to yield a row from csv file.
    The row would be a list
    """
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        line = 0
        for row in reader:
            line += 1
            if line == 1:
                continue
            yield row

def analyze(lst_of_lsts):
    start = datetime.datetime.now()
    year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }
    for lrow in lst_of_lsts:
        if lrow[5] > '00/00/2012':
            if lrow[5][6:] == '2013':
                year_count["2013"] += 1
            if lrow[5][6:] == '2014':
                year_count["2014"] += 1
            if lrow[5][6:] == '2015':
                year_count["2015"] += 1
            if lrow[5][6:] == '2016':
                year_count["2016"] += 1
            if lrow[5][6:] == '2017':
                year_count["2017"] += 1
            if lrow[5][6:] == '2018':
                year_count["2017"] += 1

    print(year_count)
    end = datetime.datetime.now()
    print("Time for counting years is {}".format(end-start))
    return (start, end, year_count)

def search_words(lst_of_lsts, key_words="ao"):
    start = datetime.datetime.now()
    found = 0
    for lst in lst_of_lsts:
        if key_words in lst[6]:
            found += 1
    print(f"{key_words} was found {found} times")
    end = datetime.datetime.now()
    print("Time for searching words is {}".format(end-start))
    return (start, end, found)

def main():
    start = datetime.datetime.now()
    filename = "exercise.csv"
    lst_of_lsts = create_list_generator(filename)
    analyze(lst_of_lsts)
    lst_of_lsts = create_list_generator(filename)
    search_words(lst_of_lsts)
    end = datetime.datetime.now()
    d = end - start
    duration = d.total_seconds()
    print(f"I revised scrip by using generator, after revised, it took {duration} second")

#from types import coroutine
async def corout_analyze(lst_of_lsts):
    analyze(lst_of_lsts)
    await asyncio.sleep(0.0)

async def corout_search(lst_of_lsts, key_words="ao"):
    search_words(lst_of_lsts, key_words="ao")
    await asyncio.sleep(0.0)

async def main_2(lst_of_lsts):
    await asyncio.gather(corout_analyze(lst_of_lsts), corout_search(lst_of_lsts, key_words="ao"))

def run_main_2():
    start = datetime.datetime.now()
    filename = "exercise.csv"
    lst_of_lsts = create_list_generator(filename)
    asyncio.run(main_2(lst_of_lsts))
    end = datetime.datetime.now()
    d = end - start
    duration = d.total_second()
    print(f"I revised scrip by using Async. After using Async, it took {duration} second")


if __name__ == "__main__":
    main()
    run_main_2()