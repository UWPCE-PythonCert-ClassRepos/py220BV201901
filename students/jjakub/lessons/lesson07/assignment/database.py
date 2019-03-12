# Database
""""
Module to configure database and logging
"""

import datetime
import logging
from pymongo import MongoClient

# Configure Monogo database
MONGO = MongoClient(host='127.0.0.1', port=27017)
DB = MONGO['HPN_database']

PRDCT = DB["product"]
CUST = DB["customer"]
RNTL = DB["rental"]

DB.PRDCT.create_index("product_id")
DB.CUST.create_index("user_id")

# Configure logging
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel("INFO")
