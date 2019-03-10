"""
lesson08, creat python code to manage inventory and customer rental infor
at csv file.
"""
import csv
from functools import partial
import logging

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

def add_furniture(customer_name, item_code, item_description, item_monthly_price, invoice_file="new_invoice"):
    """
    add single record to existing invocie file or new_invoice.csv
    """
    try:
        with open("{}.csv".format(invoice_file), mode="a") as invoice:
            invoice_writer = csv.writer(invoice, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            invoice_writer.writerow([customer_name, item_code, item_description, item_monthly_price])
            logging.info("A new record is added to invoice file")
    except Exception as e:
        print(e)

def single_customer(customer_name, invoice_file):
    """
    Input parameters: customer_name, invoice_file.
    Output: Returns a function that takes one parameter, rental_items.
    rental_items is the name of csv file
    """
    def add_new_rentals(rental_items):
        try:
            with open("{}.csv".format(invoice_file), mode="a") as invoice:
                invoice_writer = csv.writer(invoice, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                with open("{}.csv".format(rental_items), mode='r') as csv_rental:
                    csv_rental_h = csv.reader(csv_rental, delimiter=',')
                    for row in csv_rental_h:
                            row.insert(0, customer_name)
                            invoice_writer.writerow(row)
                    logging.info(f"{rental_items}.csv is imported in to invoice file")
        except Exception as e:
            print(e)
    logging.info(f"Internal state is created, Customer name is {customer_name}, invoice csv file name is {invoice_file}")
    return add_new_rentals

# #manual test
# add_furniture("test_name", "test_code", "test_description", 200, "add_furniture_output")

# Ying = single_customer("Ying", "single_customer_output")
# Ying("rental_items")