'''
Returns total price paid for individual rentals
'''

import argparse
import json
import datetime
import math
import logging

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)

log_file = 'charges_calc'+datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--log_level', help='logging level (0-3)', required=True)

    return parser.parse_args()


def load_rentals_file(filename):
    if log_level >= 3:
        logging.debug("Inside load_rentals_file() function")

    with open(filename) as file:
        try:
            data = json.load(file)
        except Exception as e:
            if log_level >= 1:
                logging.error("Hit except in load_rentals_file(), see traceback: {}".format(e))

            exit(0)

    return data


def calculate_additional_fields(data):
    if log_level >= 3:
        logging.debug("Inside calculate_additional_fields() function")

    for value in data.values():
        if (value['rental_start'] == '') or (value['rental_end'] == ''):
            if log_level >= 2:
                logging.warning("rental_start OR rental_end date missing: {}".format(value))
            continue

        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')

            if rental_start < rental_end:
                value['total_days'] = (rental_end - rental_start).days
                value['total_price'] = value['total_days'] * value['price_per_day']
                value['sqrt_total_price'] = math.sqrt(value['total_price'])
                value['unit_cost'] = value['total_price'] / value['units_rented']
            elif rental_start == rental_end:
                if log_level >= 2:
                    logging.warning("rental_start date is equal to rental_end date: {}".format(value))
                continue
            else:
                if log_level >= 2:
                    logging.warning("rental_start date is after rental_end date: {}".format(value))
                continue
        except Exception as e:
            if log_level >= 1:
                logging.error("Hit except in calculate_additional_fields(), see traceback: {}".format(e))
            continue

    return data


def save_to_json(filename, data):
    if log_level >= 3:
        logging.debug("Inside save_to_json() function")

    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    log_level = int(args.log_level)
    if log_level >= 3:
        logging.debug("args returned from parse_cmd_arguments() function {}".format(args))

    data = load_rentals_file(args.input)
    if log_level >= 3:
        logging.debug("data returned from load_rentals_file() function")

    data = calculate_additional_fields(data)
    if log_level >= 3:
        logging.debug("data returned from calculate_additional_fields() function")

    save_to_json(args.output, data)
    if log_level >= 3:
        logging.debug("returned from save_to_json() function")
