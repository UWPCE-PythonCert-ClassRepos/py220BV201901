'''
Assignment08
Yushu Song
'''

import csv
import logging
import os.path

LOGGER = logging.getLogger()
HANDLER = logging.StreamHandler()
FORMATTER = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)
LOGGER.setLevel(logging.INFO)

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    '''
    Add furniture to the invoice file given
    '''
    invoice_file = os.path.join(os.getcwd(), invoice_file)

    if os.path.isfile(invoice_file):
        mode = "a"
    else:
        mode = "w"

    try:
        with open(invoice_file, mode) as invoice_file:
            invoice_writer = csv.writer(invoice_file,
                                        delimiter=',',
                                        quotechar='"',
                                        quoting=csv.QUOTE_MINIMAL)

            invoice_writer.writerow([customer_name,
                                     item_code,
                                     item_description,
                                     item_monthly_price])

    except Exception as e:
        LOGGER.error(e)

def init_inventory():
    '''
    Initialize inventories
    '''
    invoice_file = "rented_items.csv"
    customer_names = ["Elisa Miles", "Edward Data", "Alex Gonzales"]
    item_codes = ["LR04", "KT78", "BR02"]
    item_descriptions = ["Leather Sofa", "Kitchen Table", "Queen Mattress"]
    item_monthly_prices = [25.00, 10.00, 17.00]

    for i in range(3):
        add_furniture(invoice_file,
                      customer_names[i],
                      item_codes[i],
                      item_descriptions[i],
                      item_monthly_prices[i])

def single_customer(customer_name, invoice_file):
    def create_invoice(test_file):
        # read in csv and locate the customer name
        try:
            with open(test_file, encoding='utf-8-sig', newline='') as test_invoice:
                test_data = csv.reader(test_invoice)
                for test in test_data:
                    add_furniture(invoice_file, customer_name, test[0], test[1], test[2])
        except IOError as e:
            LOGGER.error(e)
    return create_invoice

def main():
    '''
    This main flow first initialize the inventory
    Then create invoice for a single customer
    '''
    init_inventory()
    create_invoice = single_customer("Susan Wong", "rented_items.csv")
    create_invoice("test_items.csv")

if __name__ == "__main__":
    main()
