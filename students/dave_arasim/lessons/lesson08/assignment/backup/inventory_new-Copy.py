#!/usr/bin/env python
'''
Lesson 8 Assignment - Furniture Inventory
Written by David K. Arasim - 3/5/2019
'''

# Imported modules
import platform
import os
from collections import defaultdict
from functools import partial

# Global variables
this_os = platform.system()
quit_option = False

#############################################################################################
# Function section

def main():
    global quit_option

    # Build switch_dict with a dict comprehension
    switch_options = [1, 2, 3, 4]
    switch_functions = [add_furn, single_cust, create_report, quit_option_true]
    switch_dict = {sw_opt: sw_fun for sw_opt, sw_fun in zip(switch_options, switch_functions)}

    while not quit_option:
        clear_screen()

        print('*'*10,'  Main Menu  ','*'*10)
        print()
        print('1) Add Furniture')
        print('2) Single Customer')
        print('3) Create a Report')
        print('4) Quit')
        print()
        print('Choose an option: ', end='')

        user_choice = input()
        print()

        try:
            user_choice = int(user_choice)
        except ValueError:
            print('Sorry, but that is not a number')
        else:
            try:
                switch_dict.get(user_choice)()
            except TypeError:
                print('That option: ', user_choice, ' is out of range', sep='')

        print()

        if quit_option:
            print('Quitting process...')
        else:
            print('<cr> to continue... ', end='')
            input()  # input() for pause


def clear_screen():
    # Clear the screen based on operating system in use
    global this_os

    if this_os == 'Windows':
        os.system('clear')
    else:
        os.system('cls')


def add_furn():
    inv_file = input('Invoice file: ')
    cust_name = input('Customer Name: ')
    item_code = input('Item Code: ')
    item_desc = input('Item Description: ')

    got_item_price = False
    while not(got_item_price):
        item_price = input('Item Monthly Price: ')

        try:
            item_price = float(item_price)
            got_item_price = True
        except ValueError:
            print('Item Monthly Price must be a number')

    furniture_dict = add_furniture(inv_file, cust_name, item_code, item_desc, item_price)

    build_furniture_csv(furniture_dict, inv_file)
    clear_screen()


def add_furniture(inv_file, cust_name, item_code, item_desc, item_price):
    # Add to furniture dictionary from a csv file (if one exists)
    furniture_dict = defaultdict(list)
    build_furniture_dict(furniture_dict, inv_file)

    try:
        next_seq = int(max(furniture_dict.keys()) + 1)
    except ValueError:
        next_seq = 1

    furniture_dict[next_seq] = cust_name, item_code, item_desc, float(item_price)
    return furniture_dict


def build_furniture_dict(furniture_dict, inv_file):
    # Build existing furniture dictionary by extracting values from a csv file
    try:
        with open(inv_file, 'r') as dictfile:
            while True:
                furn_dict_line = dictfile.readline()
                if not furn_dict_line: break

                seq_num, cust_name, item_code, item_desc, item_price  = furn_dict_line.strip().split(',')

                furniture_dict[int(seq_num)] = cust_name, item_code, item_desc, float(item_price)

        dictfile.close()
    except FileNotFoundError:
        print()
        print(f'Furniture database {inv_file} not found.  Starting with new, empty database.')
        print('<cr> to continue...')
        input()  # input() for pause


def build_furniture_csv(furniture_dict, inv_file):
    # Export the furniture dictionary data back to a csv file
    with open(inv_file, 'w') as dictfile:
        for this_seq, this_values in furniture_dict.items():
            values_str = ','.join(str(x) for x in this_values) # Comprehension
            this_line = str(this_seq) + ',' + values_str + '\n'
            dictfile.write(this_line)

    dictfile.close()


def single_cust():
#    p_inv_file = input('Invoice file: ')
#    p_cust_name = input('Customer Name: ')
#    single_customer = partial(add_furniture, inv_file=p_inv_file, cust_name=p_cust_name)
    pass # DKA

def create_report():
    inv_file = input('Invoice file: ')
    
    try:
        with open(inv_file, 'r') as dictfile:
            print(f'\nContents of {inv_file}:') 
        
            while True:
                furn_dict_line = dictfile.readline()
                if not furn_dict_line: break

                print(furn_dict_line.strip())

        dictfile.close()
    except FileNotFoundError:
        print()
        print(f'Furniture database "{inv_file}" not found.')
        print()
        input()  # input() for pause
        clear_screen()


def quit_option_true():
    # Set quit_option to true, so function can be selected from switch_dict
    global quit_option
    quit_option = True

#############################################################################################
# Main section

if __name__ == "__main__":
    # Guards against code running automatically if this module is imported
    main()
