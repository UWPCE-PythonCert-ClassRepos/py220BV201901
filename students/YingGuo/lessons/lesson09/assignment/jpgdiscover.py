"""
a jpg discovery program in Python, using recursion
Work from a parent directory called images provided on the command line.
The program will take the parent directory as input. 
As output, it will return a list of lists structured like this: 
[“full/path/to/files”, [“file1.jpg”, “file2.jpg”,…], “another/path”,[], etc] 
"""
import argparse
import os
import logging

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

def parse_cmd_arguments():
    """
    parse command line arguments:
    -i: input file, parent directory
    C:\\gitroot\\py220BV201901\\students\\YingGuo\\lessons\\lesson09\\assignment\\data
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
    try:
        for root, dirs, files in os.walk(parent_directory):
            for dir in dirs:
                next_dir = parent_directory + f"\\{dir}"
                new_lst = lst_all_directories(next_dir)
                output_lst.extend(new_lst)
    except Exception as e:
        logging.info(f"error message is {e}")

    return output_lst

if __name__ == "__main__":
    args = parse_cmd_arguments()
    print(f"Parent directory is {args.input}")
    os.chdir(args.input)
    print("Changed current working directory to parent directory")
    out_put = lst_all_directories(args.input)
    print("Below is out put file: \n{}".format(out_put))
