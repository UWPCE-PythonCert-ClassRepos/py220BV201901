"""
HP Norton keeps pictures of all their furniture in jpg files that are
stored on their file server. They have a very crude program that starts
by discovering all directories on the server and then looking in each
of those for the jpg files. They have discovered a problem, though:
jpg files are not found when they are stored in directories that are
more than one level deep from the root directory. Your job is to:

write a jpg discovery program in Python, using recursion, that works
from a parent directory called images provided on the command line. 

The program will take the parent directory as input. 

As output, it will return a list of lists structured like this: 
[“full/path/to/files”, [“file1.jpg”, “file2.jpg”,…], 
 “another/path”,[], etc] The program must be called jpgdiscover.py
"""

from jpgdiscover import find_jpg_files
import os


def main():
    initial_path = os.getcwd()
    # initial_path += '/lessons/lesson09/assignment/data'
    initial_path += '/data'
    path_info = find_jpg_files(initial_path)
    print(path_info)

if  __name__ == '__main__':
    main()
