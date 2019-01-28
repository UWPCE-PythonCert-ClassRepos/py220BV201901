"""
    Create HP Norton database

"""

from lesson03.assignment.hpnorton_database.hpnortondbmodel import *

if __name__ == "__main__":

    DATABASE.create_tables([
        Customer
    ])

    DATABASE.close()
