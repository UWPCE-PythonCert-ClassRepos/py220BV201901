#!/usr/bin/env python3

"""
based on lesson05 MongoDB assignment.
This assignment Amend the add and update logic for both customers and products.
so that it can process these in parallel.

This module will return a list of tuples, one tuple for customer and one for products.
Each tuple will contain 4 values: 
the number of records processed (int), 
the record count in the database prior to running (int),
the record count after running (int),and the time taken to run the module (float).

a text file containing findings is also submitted.
"""

from pymongo import MongoClient
import csv
import logging
import asyncio
import datetime

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


async def customer_to_db(file_name, db_collection, when=0.0):
    """
    This function write csv file into database
    example at customers.csv
    user_id,name,address,zip_code,phone_number,email
    """
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.inventory
        db_collection = db[db_collection]

        fh = open("{}.csv".format(file_name))
        reader = csv.reader(fh)
        line = 0
        for row in reader:
            line += 1
            if line == 1:
                continue
            row_ip = {"user_id":row[0],
                        "name":row[1],
                        "address":row[2],
                        "zip_code":row[3],
                        "phone_number":row[4],
                        "email":row[5]}
            result = db_collection.insert_one(row_ip)
            logging.info(f"{row} is imported to database collection customers")
            await asyncio.sleep(when)
            #where to put this await?
        fh.close()

async def products_to_db(file_name, db_collection, when=0.0):
    """
    This function write csv file into database
    example at products.csv
    product_id,description,product_type,quantity_available
    """
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.inventory
        db_collection = db[db_collection]

        fh = open("{}.csv".format(file_name))
        reader = csv.reader(fh)
        line = 0
        for row in reader:
            line += 1
            if line == 1:
                continue
            row_ip = {"product_id":row[0],
                        "description":row[1],
                        "product_type":row[2],
                        "quantity_available":row[3]
                        }
            result = db_collection.insert_one(row_ip)
            logging.info(f"{row} is imported to database collection products")
            await asyncio.sleep(when)
        fh.close()


def show_available_products():
    """
    Returns a Python dictionary of products listed as available with the following fields:
    product_id.
    description.
    product_type.
    quantity_available.
    """
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.inventory
        products = db["products"]
        op_dict = {}
        for quantity in products.find():
            try:
                if int(quantity["quantity_available"]) > 0:
                    op_key = quantity["product_id"]
                    op_value = {"description": quantity["description"],
                    "product_type": quantity["product_type"],
                    "quantity_available": quantity["quantity_available"],
                    }
                    op_dict[op_key]= op_value
            except Exception as e:
                logging.info(e)
                logging.info(f"{quantity}is not valid data entry")
    print(op_dict)
    return op_dict


# def show_rentals():
#     """
#     Returns a Python dictionary with the following user information from users that have rented products matching product_id:
#     user_id.
#     name.
#     address.
#     phone_number.
#     email.
#     """
#     mongo = MongoDBConnection()
#     with mongo:
#         db = mongo.connection.inventory
#         rentals = db["rentals"]
#         customers = db["customers"]
#         op_dict = {}
#         for user in rentals.find():
#             query = {"user_id": user["user_id"]}
#             for customer in customers.find(query):
#                 op_key = customer["user_id"]
#                 op_value = {
#                 "name": customer["name"],
#                 "address": customer["address"],
#                 "phone_number": customer["phone_number"],
#                 "email": customer["email"]}
#                 op_dict[op_key] = op_value
#     print(op_dict)
#     return op_dict

# async def print_mdb_collection(db_collection_name, when=0.0):
#     mongo = MongoDBConnection()
#     with mongo:
#         db = mongo.connection.inventory
#         for doc in db[db_collection_name].find():
#             await asyncio.sleep(when)
#             print(doc)
async def upload_data():
    await asyncio.gather(customer_to_db("customers","customers"), products_to_db("products", "products"))

if __name__ == "__main__":
    start = datetime.datetime.now()

    mongo = MongoDBConnection()
    
    """
    async def main():
    await asyncio.gather(count(), count(), count())

    asyncio.run(main())

    await
    return?
    """
    asyncio.run(upload_data())

    """
    loop = asyncio.get_event_loop()
    loop.create_task(customer_to_db("customers","customers"))
    loop.create_task(products_to_db("products", "products"))
    loop.create_task(stop_after(loop, 3))

    loop.run_forever()
    loop.close()
    """
    end = datetime.datetime.now()
    print((start, end, (end - start)))
    show_available_products()
    # import_data("customers", "products", "rentals")
    # print_mdb_collection('customers')
    # print("show available products")
    # show_available_products()
    # print("show rentals")
    # show_rentals()

    #clean database
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.inventory
        customers = db["customers"]
        products = db["products"]
        rentals = db["rentals"]

        yorn = input("Drop data?")
        if yorn.upper() == 'Y':
            customers.drop()
            rentals.drop()
            products.drop()