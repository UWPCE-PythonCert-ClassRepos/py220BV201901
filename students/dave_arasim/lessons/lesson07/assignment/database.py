""""
MongoDB database model for Lesson 7 - serial processing (see main() below)
"""

import asyncio
import os
from datetime import datetime
from pymongo import MongoClient

program_start = datetime.now()

class MongoDBConnection(object):
    """ MongoDB Connection for content manager """

    def __init__(self, host='127.0.0.1', port=27017):
        """ Use the ip address and specific port for local windows """

        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def count_mdb_collection(collection_name):
    """ Count the particular MongoDB database collection records """

    collection_count = 0

    mongo = MongoDBConnection()

    with mongo:
        # mongodb database defined
        db = mongo.connection.media

        # collections in the MongoDB database
        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        for doc in collection_name.find():
            collection_count += 1

    return collection_count


def import_products_data(data_dir, products_file):
    """ Load MongoDB database products collection from .csv file """

    mongo = MongoDBConnection()

    with mongo:
        # mongodb database defined
        db = mongo.connection.media

        # Products collection in the MongoDB database
        products = db["products"]

        # Insert Products file records
        prod_start = datetime.now()

        add_prod = 0
        err_prod = 0

        try:
            with open(data_dir + "\\" + products_file, 'r') as csv_file:
                csv_header = csv_file.readline()

                while csv_header:
                    csv_line = csv_file.readline()
                    if not csv_line: break

                    data_in = dict(zip(csv_header.strip().split(','), csv_line.strip().split(',')))

                    try:
                        products.insert_one(data_in)
                        add_prod += 1
                    except:
                        print(f'failed to insert: {data_in}\n')
                        err_prod += 1

            csv_file.close()

        except FileNotFoundError:
            print('File not found: ', data_dir + "\\" + products_file)

        prod_finish = datetime.now()

    # Gather up the statistics to be returned
    added = (add_prod)
    errors = (err_prod)
    elapsed = (prod_finish - prod_start).total_seconds()

    return added, errors, elapsed


def import_customers_data(data_dir, customers_file):
    """ Load MongoDB database customers collection from .csv file """

    mongo = MongoDBConnection()

    with mongo:
        # mongodb database defined
        db = mongo.connection.media

        # Customers collection in the MongoDB database
        customers = db["customers"]

        # Insert Customers file records
        cust_start = datetime.now()

        add_cust = 0
        err_cust = 0

        try:
            with open(data_dir + "\\" + customers_file, 'r') as csv_file:
                csv_header = csv_file.readline()

                while csv_header:
                    csv_line = csv_file.readline()
                    if not csv_line: break

                    data_in = dict(zip(csv_header.strip().split(','), csv_line.strip().split(',')))

                    try:
                        customers.insert_one(data_in)
                        add_cust += 1
                    except:
                        print(f'failed to insert: {data_in}\n')
                        err_cust += 1

            csv_file.close()

        except FileNotFoundError:
            print('File not found: ', data_dir + "\\" + customers_file)

        cust_finish = datetime.now()

    # Gather up the statistics to be returned
    added = (add_cust)
    errors = (err_cust)
    elapsed = (cust_finish - cust_start).total_seconds()

    return added, errors, elapsed


def import_rentals_data(data_dir, rentals_file):
    """ Load MongoDB database rentals collection from .csv file """

    mongo = MongoDBConnection()

    with mongo:
        # mongodb database defined
        db = mongo.connection.media

        # Rentals collection in the MongoDB database
        rentals = db["rentals"]

        # Insert Rentals file records
        rent_start = datetime.now()

        add_rent = 0
        err_rent = 0

        try:
            with open(data_dir + "\\" + rentals_file, 'r') as csv_file:
                csv_header = csv_file.readline()

                while csv_header:
                    csv_line = csv_file.readline()
                    if not csv_line: break

                    data_in = dict(zip(csv_header.strip().split(','), csv_line.strip().split(',')))

                    try:
                        rentals.insert_one(data_in)
                        add_rent += 1
                    except:
                        print(f'failed to insert: {data_in}\n')
                        err_rent += 1

            csv_file.close()

        except FileNotFoundError:
            print('File not found: ', data_dir + "\\" + rentals_file)

        rent_finish = datetime.now()

    # Gather up the statistics to be returned
    added = (add_rent)
    errors = (err_rent)
    elapsed = (rent_finish - rent_start).total_seconds()

    return added, errors, elapsed


async def import_products_async(data_dir, products_file):
    """ Load MongoDB database products collection from .csv file """

    print('inside import_products_async\n')
    await asyncio.sleep(0)

    mongo = MongoDBConnection()

    with mongo:
        # mongodb database defined
        db = mongo.connection.media

        # Products collection in the MongoDB database
        products = db["products"]

        # Insert Products file records
        prod_start = datetime.now()

        add_prod = 0
        err_prod = 0

        try:
            with open(data_dir + "\\" + products_file, 'r') as csv_file:
                csv_header = csv_file.readline()

                while csv_header:
                    csv_line = csv_file.readline()
                    if not csv_line: break

                    data_in = dict(zip(csv_header.strip().split(','), csv_line.strip().split(',')))

                    try:
                        products.insert_one(data_in)
                        add_prod += 1
                    except:
                        print(f'failed to insert: {data_in}\n')
                        err_prod += 1

            csv_file.close()

        except FileNotFoundError:
            print('File not found: ', data_dir + "\\" + products_file)

        prod_finish = datetime.now()

    # Gather up the statistics to be returned
    added = (add_prod)
    errors = (err_prod)
    elapsed = (prod_finish - prod_start).total_seconds()

    print('done with import_products_async\n')
    return added, errors, elapsed


async def import_customers_async(data_dir, customers_file):
    """ Load MongoDB database customers collection from .csv file """

    print('inside import_customers_async\n')
    await asyncio.sleep(0)

    mongo = MongoDBConnection()

    with mongo:
        # mongodb database defined
        db = mongo.connection.media

        # Customers collection in the MongoDB database
        customers = db["customers"]

        # Insert Customers file records
        cust_start = datetime.now()

        add_cust = 0
        err_cust = 0

        try:
            with open(data_dir + "\\" + customers_file, 'r') as csv_file:
                csv_header = csv_file.readline()

                while csv_header:
                    csv_line = csv_file.readline()
                    if not csv_line: break

                    data_in = dict(zip(csv_header.strip().split(','), csv_line.strip().split(',')))

                    try:
                        customers.insert_one(data_in)
                        add_cust += 1
                    except:
                        print(f'failed to insert: {data_in}\n')
                        err_cust += 1

            csv_file.close()

        except FileNotFoundError:
            print('File not found: ', data_dir + "\\" + customers_file)

        cust_finish = datetime.now()

    # Gather up the statistics to be returned
    added = (add_cust)
    errors = (err_cust)
    elapsed = (cust_finish - cust_start).total_seconds()

    print('done with import_customers_async\n')
    return added, errors, elapsed


async def import_rentals_async(data_dir, rentals_file):
    """ Load MongoDB database rentals collection from .csv file """

    print('inside import_rentals_async\n')
    await asyncio.sleep(0)

    mongo = MongoDBConnection()

    with mongo:
        # mongodb database defined
        db = mongo.connection.media

        # Rentals collection in the MongoDB database
        rentals = db["rentals"]

        # Insert Rentals file records
        rent_start = datetime.now()

        add_rent = 0
        err_rent = 0

        try:
            with open(data_dir + "\\" + rentals_file, 'r') as csv_file:
                csv_header = csv_file.readline()

                while csv_header:
                    csv_line = csv_file.readline()
                    if not csv_line: break

                    data_in = dict(zip(csv_header.strip().split(','), csv_line.strip().split(',')))

                    try:
                        rentals.insert_one(data_in)
                        add_rent += 1
                    except:
                        print(f'failed to insert: {data_in}\n')
                        err_rent += 1

            csv_file.close()

        except FileNotFoundError:
            print('File not found: ', data_dir + "\\" + rentals_file)

        rent_finish = datetime.now()

    # Gather up the statistics to be returned
    added = (add_rent)
    errors = (err_rent)
    elapsed = (rent_finish - rent_start).total_seconds()

    print('done with import_rentals_async\n')
    return added, errors, elapsed


def drop_data():
    """ Drop entire MongoDB database collection """

    mongo = MongoDBConnection()

    with mongo:
        # mongodb database defined
        db = mongo.connection.media

        # collections in the MongoDB database
        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        products.drop()
        customers.drop()
        rentals.drop()


def main():
    """ Extra testing scenarios...also works with pytest 'test_gradel07.py' """

    import_elapsed = 0

    mongo = MongoDBConnection()

    with mongo:
        # mongodb database defined
        db = mongo.connection.media

        # collections in the MongoDB database
        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        print(f'Products count: {count_mdb_collection(products)}')
        print(f'Customers count: {count_mdb_collection(customers)}')
        print(f'Rentals count: {count_mdb_collection(rentals)}\n')

        data_dir = os.path.dirname(os.path.abspath(__file__))

        added, errors, elapsed = import_products_data(data_dir, "products.csv")
        import_elapsed += elapsed
        print(f'Added Products records: {added}')
        print(f'Error Products records: {errors}')
        print(f'Elapsed Products time: {elapsed}\n')

        added, errors, elapsed = import_customers_data(data_dir, "customers.csv")
        import_elapsed += elapsed
        print(f'Added Customers records: {added}')
        print(f'Error Customers records: {errors}')
        print(f'Elapsed Customers time: {elapsed}\n')

        added, errors, elapsed = import_rentals_data(data_dir, "rentals.csv")
        import_elapsed += elapsed
        print(f'Added Rentals records: {added}')
        print(f'Error Rentals records: {errors}')
        print(f'Elapsed Rentals time: {elapsed}\n')

        print(f'Products count: {count_mdb_collection(products)}')
        print(f'Customers count: {count_mdb_collection(customers)}')
        print(f'Rentals count: {count_mdb_collection(rentals)}\n')

        program_finish = datetime.now()
        program_elapsed = (program_finish - program_start).total_seconds()
        print(f'Elapsed program time: {program_elapsed}')
        print(f'Elapsed import time: {import_elapsed}')
        print(f'Elapsed overhead time: {(program_elapsed - import_elapsed)}\n')

        # Option to drop data from collections
        yorn = input("Drop data?")

        if yorn.upper() == 'Y':
            drop_data()


if __name__ == "__main__":
    main()
