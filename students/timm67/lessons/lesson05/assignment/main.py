from loguru import logger
from sys import stdout

from ingest_csv import ingest_csv

from database import MongoDBConnection

def main():
    """
    Ensure you application will create an empty database if one doesn’t exist
    when the app is first run. Call it customers.db
    """

    # Standalone function to initialize logging
    logger.add(stdout, level='WARNING')
    logger.add("logfile_{time}.txt", level='INFO')
    logger.enable(__name__)

    with MongoDBConnection():
        ingest_csv()


if  __name__ == '__main__':
    main()
