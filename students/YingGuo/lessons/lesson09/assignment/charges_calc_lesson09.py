'''
Returns total price paid for individual rentals
make logging selective, by using decorators.
Add decorator(s) to introduce conditional logging
so that a single command line variable can turn logging on or off for decorated classes or functions.
'''
import argparse
import json
import datetime
import math
import logging

def parse_cmd_arguments():
    """
    parse command line arguments:
    -i: input file
    -o: output file
    -d: logging level
    """
    logging.info("argument parse from command line, -i is input file, -o is output file, -d is logging.")
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', required=False, help='log level. Can be 0-3. Defaults to 0')

    return parser.parse_args()

def decorator_logging_parameter(Level_number=0):
    """
    set logging level:
    0: No debug messages or log file.
    1: Only error messages.
    2: Error messages and warnings.
    3: Error messages, warnings and debug messages.
    """
    def set_logging_level(func):
        if Level_number == 0:
            return func
        if Level_number != 0:
            log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
            formatter = logging.Formatter(log_format)
            #log_file = datetime.datetime.now().strftime(“%Y-%m-%d”)+’.log’
            file_handler = logging.FileHandler("charges_calc.log")
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            if Level_number == 1:
                file_handler.setLevel(logging.ERROR)
                console_handler.setLevel(logging.ERROR)
            elif Level_number == 2:
                file_handler.setLevel(logging.WARNING)
                console_handler.setLevel(logging.WARNING)
            elif Level_number == 3:
                file_handler.setLevel(logging.DEBUG)
                console_handler.setLevel(logging.DEBUG)
            
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
            return func
    return set_logging_level

logging.info("Called argment parse function")
args = parse_cmd_arguments()

@decorator_logging_parameter(args.debug)
def load_rentals_file(filename):
    """load data into file"""
    logging.info("load json file into data")
    with open(filename) as file:
        try:
            data = json.load(file)
        except:
            exit(0)
    return data

@decorator_logging_parameter(args.debug)
def validate_entry(value, index):
    try:
        rental_start = datetime.datetime.strptime(value['rental_start'],
                                                  '%m/%d/%y')
    except ValueError:
        logging.warning('Unable to process entry %d because rental start ' +
                        'is not in %%m/%%d/%%y format. Skipping...', index)
        return False

    try:
        rental_end = datetime.datetime.strptime(value['rental_end'],
                                                '%m/%d/%y')
    except ValueError:
        logging.warning('Unable to process entry %d because rental end ' +
                        'is not in %%m/%%d/%%y format. Skipping...', index)
        return False

    if rental_end < rental_start:
        logging.warning('Unable to process entry %d because ' +
                        'rental start > end. Skipping...', index)
        return False

    if value['price_per_day'] < 0:
        logging.warning('Unable to process entry %d because ' +
                        'price per day is negative. Skipping...', index)
        return False

    if value['units_rented'] <= 0:
        logging.warning('Unable to process entry %d because ' +
                        'units rented is non-positive. Skipping...', index)
        return False

    return True

@decorator_logging_parameter(args.debug)
def calculate_additional_fields(data):
    logging.debug('Calculating additional fields for %d entries',
                  len(data.values()))
    for index, value in enumerate(data.values()):
        logging.debug('Processing entry %d with value: %s', index, value)
        try:
            if not validate_entry(value, index):
                continue
            rental_start = datetime.datetime.strptime(value['rental_start'],
                                                      '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'],
                                                    '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days + 1
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except:
            logging.warning('Unexpected failure processing entry %d. Skipping',
                            index)
            continue

    return data

@decorator_logging_parameter(args.debug)
def save_to_json(filename, data):
    """write output data into json file"""
    logging.info("Write out put to json file")
    with open(filename, 'w') as file:
        json.dump(data, file)


# logging.info("Called logging level function")
# set_logging_level(args.debug)
logging.info("Called load_rentals_file function")
data = load_rentals_file(args.input)
logging.info("Called calculate_additional_fields function")
data = calculate_additional_fields(data)
logging.info("Called saving output function")
save_to_json(args.output, data)
