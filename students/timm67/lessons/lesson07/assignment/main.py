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

    ret_list_linear = linear()

    logger.info("Start parallel ingest from CSV files")

    ret_list_parallel = parallel()

    logger.info("CSV ingest completed")

    logger.info("Linear ingest statistics:")
    logger.info(f"Customer db: num records[{ret_list_linear[0][0]}]")
    logger.info(f"Customer db: time elapsed[{ret_list_linear[0][3]}]")
    logger.info(f"Product db:  num records[{ret_list_linear[1][0]}]")
    logger.info(f"Product db:  time elapsed[{ret_list_linear[1][3]}]")
    logger.info(f"Rental db:   num records[{ret_list_linear[2][0]}]")
    logger.info(f"Product db:  time elapsed[{ret_list_linear[2][3]}]")

    logger.info("Parallel ingest statistics:")
    logger.info(f"Customer db: num records[{ret_list_parallel[0][0]}]")
    logger.info(f"Customer db: time elapsed[{ret_list_parallel[0][3]}]")
    logger.info(f"Product db:  num records[{ret_list_parallel[1][0]}]")
    logger.info(f"Product db:  time elapsed[{ret_list_parallel[1][3]}]")
    logger.info(f"Rental db:   num records[{ret_list_parallel[2][0]}]")
    logger.info(f"Product db:  time elapsed[{ret_list_parallel[2][3]}]")

if  __name__ == '__main__':
    main()
