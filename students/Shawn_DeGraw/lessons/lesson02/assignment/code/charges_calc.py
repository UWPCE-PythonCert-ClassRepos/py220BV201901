'''
Returns total price paid for individual rentals
'''


import argparse
import json
import datetime
import math
import logging

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
LOG_LEVEL = {'0': 'CRITICAL', '1': 'ERROR', '2': 'WARNING', '3': 'DEBUG'}

FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


def parse_cmd_arguments():
    """
    Usage: prog -i,--input INFILE -o,--output OUTFILE -d,-debug LEVEL

    Arguments:
        INFILE  filename for input data file
        OUTFILE filename for output data file
        LEVEL   debug level

    Options:
        -i, --input options for input file
        -o, --output options for output file
        -d, -debug options for debug level
    """

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '-debug', help='debug level 0=none, 1=error, 2=warn, 3=debug', default='0', required=False)

    return parser.parse_args()


def load_rentals_file(filename):
    """ Read json input file and create data structure """

    with open(filename) as file:
        logging.debug(f'Reading data from file: {filename}')
        try:
            newdata = json.load(file)
        except FileNotFoundError as file_error:
            logging.error(f"Input file not found: {type(file_error).__name__}")
            exit(1)
        except EOFError as eof_error:
            logging.error(f"Input file read error: {type(eof_error).__name__}")
            exit(2)
    return newdata

def calculate_additional_fields(data):
    """ Calculate data using input data """

    logging.debug('Calculating new data.')
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            if rental_start > rental_end:
                logging.warning("Rental start date is after rental end date.")
                raise ValueError
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError as data_error:
            logging.error(f"Bad data in file. Skipping data: {value}")
            continue

    return data

def save_to_json(filename, data):
    """ Save new calculations to file """

    logging.debug(f'Writing calculated data to file: {filename}')
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":

    args = parse_cmd_arguments()

    LOGGER.setLevel(LOG_LEVEL.get(args.d, "WARNING"))

    logging.debug(f"Program arguments: input file = {args.input}, output file = {args.output}, debug level = {args.d}")

    DATA = load_rentals_file(args.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(args.output, DATA)
