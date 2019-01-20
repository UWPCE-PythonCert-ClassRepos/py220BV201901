'''
Returns total price paid for individual rentals 
'''


import argparse
import json
import datetime
import math
import logging

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
log_level = {'0': 'CRITICAL', '1': 'ERROR', '2': 'WARNING', '3': 'DEBUG'}

formatter = logging.Formatter(log_format)

file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '-debug', help='debug level 0=none,1=error,2=warn,3=debug', default='0',required=False)

    return parser.parse_args()


def load_rentals_file(filename):
    with open(filename) as file:
        try:
            data = json.load(file)
        except Exception as exerror:
            logging.error(f"Input file read error: {type(exerror).__name__}")
            exit(0)
    return data

def calculate_additional_fields(data):
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except:
            logging.error(f"Bad data in file. Skipping data: {value}")
            continue

    return data

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":

    args = parse_cmd_arguments()

    console_handler.setLevel(log_level.get(args.d, "ERROR"))
    file_handler.setLevel(log_level.get(args.d, "ERROR"))

    logging.debug(f"Program arguments: input file = {args.input}, output file = {args.output}, debug level = {args.d}")

    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
