"""
    Create HP Norton database

"""

from lesson03.assignment.hpnorton_database.hpnortondbmodel import *

if __name__ == "__main__":

    try:
        DATABASE.connect()
        DATABASE.create_tables([
            Customer
        ])
    except InternalError:
        print("Database Error.")

    DATABASE.close()
