import sys

from loguru import logger

from inventory import add_furniture
from inventory import single_customer

# Standalone function to initialize logging
logger.add(sys.stdout, level='WARNING')
logger.add("logfile_{time}.txt", level='INFO')
logger.enable(__name__)

def main():
    pass

if  __name__ == '__main__':
    main()
