"""
a jpg discovery program in Python, using recursion
Work from a parent directory called images provided on the command line.
The program will take the parent directory as input. 
As output, it will return a list of lists structured like this: 
[“full/path/to/files”, [“file1.jpg”, “file2.jpg”,…], “another/path”,[], etc] 
"""
import argparse
import os

def parse_cmd_arguments():
    """
    parse command line arguments:
    -i: input file, parent directory
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='parent directory', required=True)

    return parser.parse_args()

def lst_all_directories(parent_directory):
    """
    list all files in all directories under cwd
    """
    os.chdir(parent_directory)
    current_dir = [os.getcwd()]
    lst = [os.listdir()]
    output_lst = current_dir + lst
    for root, dirs, files in os.walk("."):
        for rt in root:
            output_lst += lst_all_directories(root)
    return output_lst


if __name__ == "__main__":
    args = parse_cmd_arguments()
    print(f"Parent directory is {args.input}")
    os.chdir(args.input)
    print("Changed current working directory to parent directory")
    out_put = lst_all_directories(args.input)
    print(out_put)
