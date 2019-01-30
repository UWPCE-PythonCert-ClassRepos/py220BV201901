'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
from loguru import logger


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='out JSON file', required=True)
    parser.add_argument('-l', '--level', help="debug level", required=True)
    return parser.parse_args()


def load_rentals_file(filename):
    with open(filename) as file:
        try:
            data = json.load(file)
        except ValueError:
            logger.error('JSON syntax error')
            exit(0)
    return data


def calculate_additional_fields(data):
    record_num = 0
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    for value in data.values():
        logger.debug(f"record num: {record_num}")
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'],
                                                      '%m/%d/%y')
        except ValueError:
            if (value['rental_start'] == ''):
                logger.warning("rental start not present! Using today's date")

                value['rental_start'] = "{0}/{1}/{2}".format(month, day, year)
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'],
                                                    '%m/%d/%y')
        except ValueError:
            if (rental_end == ''):
                logger.warning("rental end not present! Using today's date")
                value['rental_end'] = "{0}/{1}/{2}".format(month, day, year)
        value['total_days'] = abs((rental_end - rental_start).days)
        logger.debug(f"total days: {value['total_days']}")
        value['total_price'] = value['total_days'] * value['price_per_day']
        value['sqrt_total_price'] = math.sqrt(value['total_price'])
        if (value['units_rented'] == 0):
            logger.warning("units_rented is zero; using 1 as substitute")
            value['units_rented'] = 1
        value['unit_cost'] = value['total_price'] / value['units_rented']
        record_num += 1
    return data


def save_to_json(filename, data):
    with open(filename, 'w') as file:
        try:
            json.dump(data, file)
        except TypeError:
            logger.error("JSON serialization error")


if __name__ == "__main__":
    logger.enable('__main__')
    args = parse_cmd_arguments()
    print(f"Debug level: {args.level}")
    logger.add("debugger_log_{time}.txt")

    #
    # log levels per the assignment
    # 0: No debug messages or log file.
    # 1: Only error messages.
    # 2: Error messages and warnings.
    # 3: Error messages, warnings and debug messages.
    #

    if args.level == 0:
        logger.disable('__main__')
    elif args.level == 1:
        logger.level = logger.error
        logger.add("debugger_log_{time}.txt", level=logger.error)
    elif args.level == 2:
        logger.level = logger.warning
        logger.add("debugger_log_{time}.txt", level=logger.warning)
    elif args.level == 3:
        logger.level = logger.debug
        logger.add("debugger_log_{time}.txt", level=logger.debug)
    else:
        pass

    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
    logger.debug(f"data saved to {args.output}")
