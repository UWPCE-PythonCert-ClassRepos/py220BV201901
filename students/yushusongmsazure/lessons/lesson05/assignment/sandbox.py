
import csv
import os
from database import MongoDBConnection





def import_data(directory_name, product_file, customer_file, rentals_file):
    mongo = MongoDBConnection()
    with mongo:
        # mongodb database; it all starts here
        db = mongo.connection.inventory
        # collection in database


        with open(os.path.join(directory_name, customer_file),
                encoding='utf-8-sig',
                newline='') as csvfile:

            customer_data = csv.DictReader(csvfile)
            customer_col = db["customers"]
            for row in customer_data:
                customer_col.insert_one(row)





        # for row in customers_data:
        #     # print(row)
        #     print(row['user_id'], row['name'], row['address'], row['zip_code'], row['phone_number'], row['email'])



# def print_mdb_collection(collection_name):
#     for doc in collection_name.find():
#         print(doc)

def main():
    import_data(os.path.dirname(os.path.abspath(__file__)),
                'products.csv',
                'customers.csv',
                'rentals.csv')


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
#         collector.drop()

# # of course!
 
if __name__== "__main__":
    main()