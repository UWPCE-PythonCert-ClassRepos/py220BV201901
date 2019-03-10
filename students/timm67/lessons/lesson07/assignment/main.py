import sys

from loguru import logger

from linear import linear
from parallel import parallel

from models import util_drop_all
from database import Connection

# Standalone function to initialize logging
logger.add(sys.stdout, level='WARNING')
logger.add("logfile_{time}.txt", level='INFO')
logger.enable(__name__)

def main():
    """
    Ensure you application will create an empty database if one doesn’t exist
    when the app is first run. Call it customers.db
    """

    logger.info("Start linear ingest from CSV files")

    linear()

    logger.info("Start parallel ingest from CSV files")

    parallel()

if  __name__ == '__main__':
    main()
