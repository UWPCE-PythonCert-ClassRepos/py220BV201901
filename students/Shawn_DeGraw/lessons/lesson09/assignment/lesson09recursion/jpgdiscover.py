""" Class for directory recursion """

from pathlib import Path
import os
import argparse
import logging
import datetime


LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel("DEBUG")
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


class DirectoryRecursion:
    """ Class to search for file extension """

    def __init__(self, parent_directory):
        self.parent_directory = Path(parent_directory)
        self.file_result = []

    def list_files(self, path, total_path):
        """ recursive search of files """

        LOGGER.info(f'Working in directory: {path}')
        directory_listing = []
        file_list = []

        for item in os.listdir(path):
            directory_item = os.path.join(path, item)

            if os.path.isfile(directory_item):

                if item.lower().endswith("png"):
                    LOGGER.debug(f'File found: {directory_item}')
                    file_list.append(item)

            elif os.path.isdir(directory_item):
                LOGGER.info(f'Directory found: {directory_item}')
                directory_listing.append(directory_item)

            else:
                LOGGER.info(f'Who knows what this is: {item}')

        total_path.append(path)
        total_path.append(file_list)

        if len(directory_listing):
            # do recursive calls if sub directories found
            for directory in directory_listing:
                self.list_files(directory, total_path)

        return total_path

def parse_cmd_arguments():
    """
    Usage: prog -d, DIRECTORY

    Arguments:
        DIRECTORY  directory to search

    Options:
        -d options for directory
    """

    parser = argparse.ArgumentParser(description='Process a directory.')
    parser.add_argument('-d', help='Directory to search', default=os.getcwd(), required=False)

    return parser.parse_args()


if __name__ == "__main__":

    total_path = []
    ARGS = parse_cmd_arguments()
    new_listing = DirectoryRecursion(ARGS.d)

    result = new_listing.list_files(new_listing.parent_directory, total_path)

    print(result)
