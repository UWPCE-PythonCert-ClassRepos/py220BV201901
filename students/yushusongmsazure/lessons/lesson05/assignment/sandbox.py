
import csv
import os
from database import MongoDBConnection

def import_data(directory_name, product_file, customer_file, rentals_file):
    mongo = MongoDBConnection()
    with mongo:
        # mongodb database; it all starts here
        db = mongo.connection.inventory
        # collection in database

        # process customers data
        with open(os.path.join(directory_name, customer_file),
                encoding='utf-8-sig',
                newline='') as csvfile:

            # add customer collection
            customer_data = csv.DictReader(csvfile)
            customer_col = db["customers"]
            for row in customer_data:
                customer_col.insert_one(row)

        # process products data
        with open(os.path.join(directory_name, product_file),
                encoding='utf-8-sig',
                newline='') as prod_file:

            # add customer collection
            prod_data = csv.DictReader(prod_file)
            prod_col = db["products"]

            for row in prod_data:
                quantity = int(row["quantity_available"])
                prod_col.insert_one({"product_id":row["product_id"],
                                     "description":row["description"],
                                     "product_type":row["product_type"],
                                     "quantity_available":quantity})

        # process rentals data
        with open(os.path.join(directory_name, rentals_file),
                encoding='utf-8-sig',
                newline='') as rent_file:

            # add customer collection
            rent_data = csv.DictReader(rent_file)
            rent_col = db["rentals"]
            rent_col.insert_many(rent_data)

def show_available_products():
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.inventory
        prod_col = db["products"]
        products={}

        for a in prod_col.find({"quantity_available": {"$gt": 0}}):
            products[a["product_id"]] = {"description":a["description"],"product_type":a["product_type"],"quantity_available":a["quantity_available"]}
        
        return products

        # prod_col.find({quantity_available : {$gt:0}})
        # print_mdb_collection(t)
        # for prod in prod_col.find():
        #     if int(prod["quantity_available"]) > 0:

def show_rentals(product_id):
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.inventory
        prod_col = db["products"]
        users={}

def main():
    import_data(os.path.dirname(os.path.abspath(__file__)),
                'products.csv',
                'customers.csv',
                'rentals.csv')
    show_available_products()

#         # notice how easy these are to create and that they are "schemaless"
#         # that is, the Python module defines the data structure in a dict,
#         # rather than the database which just stores what it is told
 
#         cd_ip = {"artist": "The Who", "Title": "By Numbers"}
#         result = cd.insert_one(cd_ip)

#         cd_ip = [
#             {"artist": "Deep Purple", "Title": "Made In Japan", "name": "Andy"},
#             {"artist": "Led Zeppelin", "Title": "House of the Holy", "name": "Andy"},
#             {"artist": "Pink Floyd", "Title": "DSOM", "name": "Andy"},
#             {"artist": "Albert Hammond", "Title": "Free Electric Band", "name": "Sam"},
#             {"artist": "Nilsson", "Title": "Without You", "name": "Sam"}]

#         result = cd.insert_many(cd_ip)
 
#         print_mdb_collection(cd)
 
#         # another collection
#         collector = db["collector"]
#         collector_ip = [
#             {"name": "Andy", "preference": "Rock"},
#             {"name": "Sam", "preference": "Pop"}]
 
#         result = collector.insert_many(collector_ip)
 
#         print_mdb_collection(collector)
#         # related data
#         for name in collector.find():
#             print(f'List for {name["name"]}')
#             query = {"name": name["name"]}
#             for a_cd in cd.find(query):
#                 print(f'{name["name"]} has collected {a_cd}')

#         # start afresh next time?
#         yorn = input("Drop data?")
#         if yorn.upper() == 'Y':
#             cd.drop()
#             collector.drop()

 
if __name__== "__main__":
    main()