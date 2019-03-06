'''
PY220BV201901
Jason Jakubiak
Returns total price paid for individual rentals
'''

import logging
import argparse
import json
import datetime
import math

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.WARNING)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
CONSOLE_HANDLER.setLevel(logging.DEBUG)

LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


def main():
    """ calls functions in module """
    args = parse_cmd_arguments()
    debug_level(args.debug)
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)


def parse_cmd_arguments():
    """
    invoke command line parser
    options: input, output, debug level
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='level 0=none, 1=error, 2=warning, 3=debug'
                        , default=0, required=False)
    return parser.parse_args()


def debug_level(lvl):
    """ return debug level argument """
    level_dict = {0: 'NONE', 1: 'ERROR', 2: 'WARNING', 3: 'DEBUG'}
    log_level = level_dict.get(int(lvl))
    if int(lvl) == 0:
        LOGGER.disabled = True
        LOGGER.debug("Logger disabled")
    else:
        LOGGER.setLevel(log_level)
        LOGGER.debug(f"Logger level set to: {log_level}")


def load_rentals_file(filename):
    """ open and load source file """
    with open(filename) as file:
        try:
            data = json.load(file)
            LOGGER.debug("Loaded source file")
        except:
            LOGGER.warning("Failed: load source file")
            exit(0)
    return data


def calculate_additional_fields(data):
    """ create additional data attributes """
    for index, value in enumerate(data.values()):
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
            LOGGER.debug(f"Load success: #{index + 1}, {value}")
        except:
            LOGGER.error(f"Load failed, non-conforming data: #{index + 1}, {value}")
            continue

    return data


def save_to_json(filename, data):
    """ save parsed data to file """
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
            LOGGER.debug("Loaded source file")
    except:
        LOGGER.warning("Failed: save source file")

if __name__ == "__main__":
    main()
