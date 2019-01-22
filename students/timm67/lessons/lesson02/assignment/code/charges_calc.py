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
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
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
    for value in data.values():
        try:
            logger.debug(f"record num: {record_num}")
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            logger.debug(f"rental start: {rental_start}")
            logger.debug(f"rental end: {rental_end}")
            value['total_days'] = abs((rental_end - rental_start).days)
            logger.debug(f"total days: {value['total_days']}")
            value['total_price'] = value['total_days'] * value['price_per_day']
            logger.debug(f"total price: {value['total_price']}")
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            logger.debug(f"total price sqrt: {value['sqrt_total_price']}")
            if (value['units_rented'] == 0):
                logger.warning("units_rented is zero; using 1 as substitute")
                value['units_rented'] = 1
            value['unit_cost'] = value['total_price'] / value['units_rented']
            logger.debug(f"unit cost: {value['unit_cost']}")
        except ValueError:
            logger.error("negative square root or invalid date")
            exit(0)
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
    logger.add("dbgfile_{time}.log")
    logger.info('logger enabled')
    args = parse_cmd_arguments()
    logger.debug(f"Input arg: {args.input}")
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
    logger.debug(f"data saved to {args.output}")
