#! usr/bin/env python
'''
Returns total price paid for individual rentals
Debugging / logging assignment by Arun Nalla
'''

import argparse
import json
import datetime
import math
import logging


log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
formatter = logging.Formatter(log_format)

file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.WARNING)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def parse_cmd_arguments():
    """ use argparse to enter command line
    entry of input and output file"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help="debug levels", type=int,
                        choices=[0, 1, 2, 3], required=False)
    logger.debug("added command line arguments for input and output files")
    return parser.parse_args()


def load_rentals_file(filename):
    """ open source file"""
    with open(filename) as file:
        logger.debug('This is the source file {}'.format(filename))
        try:
            data = json.load(file)
            logger.debug('Source file : {} has been uploaded'.format(filename))
        except FileNotFoundError:
            logger.error("Please check the input source file")
    return data

def calculate_additional_fields(data):
    """calculate the rental price modify data with new information
    check for errors in start and end dates"""

    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            if value['total_days'] < 0:
                logger.warning("Error in either rental start or end dates")
                raise ValueError
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
            #exit(0)
        except ValueError:
            logger.error("Incomplte data in the out file for the item {}".format(value))

    return data

def save_to_json(filename, data):
    """ save the updated data as new file"""
    with open(filename, 'w') as file:
        logger.debug("The data has been saved as an output with a file_name: {}".format(filename))
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    logger.debug("The source file: {} and the output file ios {}".format(args.input, args.output))
    if args.debug == 0:
        logger.setLevel(logging.INFO)
    elif args.debug == 1:
        logger.setLevel(logging.ERROR)
    elif args.debug == 2:
        logger.setLevel(logging.WARNING)
    elif args.debug == 3:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO) # not working as expected, needs changes

    input_data = load_rentals_file(args.input)
    output_data = calculate_additional_fields(input_data)
    save_to_json(args.output, output_data)

