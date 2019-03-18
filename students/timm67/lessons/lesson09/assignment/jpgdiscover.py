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

import os
import sys
from queue import Queue


def find_jpg_files(initial_path):
    dir_list = []

    def find_jpg_recursive(cur_path, dir_list):
        dir_list.append(cur_path)
        file_list = []
        for filename in os.listdir(cur_path):
            print(f'0 Searching file/dir {filename}')
            if filename.endswith('.png'):
                file_list.append(filename)
        dir_list.append(file_list)
        for filename in os.listdir(cur_path):
            if os.path.isdir(cur_path + os.sep + filename) is True:
                next_dir = cur_path + os.sep + filename
                print(f'1 Searching dir {next_dir}')
                find_jpg_recursive(next_dir, dir_list)
    find_jpg_recursive(initial_path, dir_list)
    return dir_list
