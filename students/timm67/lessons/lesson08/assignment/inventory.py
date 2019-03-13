from functools import partial

def import_csv_gen(csv_filename):
    """
    Import csv file generator (yields one record per yield)
    """
    with open(csv_filename, 'r') as csv_fd:
        line = 'foo'
        while line:
            try:
                line = csv_fd.readline()
                # generator 'yield' statement for each
                # line of the CSV file below. Python CSV
                # support does not allow per-line parsing
                yield line.rstrip('\n').split(',')
            except EOFError:
                return

def import_customer_csv():
    """
    Ingest csv function to combine extract and import gen functions,
    and populate data from generator in database
    """
    # Create a CSV import generator (next yields one db row)
    import_generator = import_csv_gen(EXTRACT_PATH + CUST_CSV_FILENAME)
    # Iterate over all other rows
    while True:
        try:
            data = next(import_generator)
            if len(data) != 8:
                logger.error(f'Data item count: {len(data)}')
                continue
        except StopIteration:
            break


"""
Input paramters: invoice_file, customer_name, item_code
    item_description, item_monthly_price

This function will create invoice_file if it doesn’t exist
or append a new line to it if it does. After adding a few
items to the same file, the file created by add_furniture
should look something like this:

Elisa Miles,LR04,Leather Sofa,25.00
Edward Data,KT78,Kitchen Table,10.00
Alex Gonzales,BR02,Queen Mattress,17.00
"""
def add_furniture(invoice_file, customer_name, item_code,
                  item_description, item_monthly_price):
    with open(invoice_file, 'a+') as fp:

    pass


"""
Input parameters: invoice_file, customer_name
Output: Returns a function that takes one parameter, rental_items.

single_customer needs to use functools.partial and closures, 
in order to return a function that will iterate through rental_items 
and add each item to invoice_file.
"""
def single_customer(invoice_file, customer_name):
    pass
