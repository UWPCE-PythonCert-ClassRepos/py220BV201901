# Launches the user interface for the inventory management system
"""
Module for the user intergace of the invenotry mangement system
"""

import sys
from inventory_management.market_prices import get_latest_price
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances


def main_menu(user_prompt=None):
    """
    Function for the main menu
    """
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())


    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print(f"Please choose from the following options ({options_str}):")
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)


def get_market_price(item_code):
    """
    Function to latest item price, calls get_latest price from market_prices module
    """
    item_price = get_latest_price(item_code)
    return item_price


def add_new_item():
    """
    Function prompt user for item attributes and add item to Full Inventory
    """
    item_code = input("Enter item code: ")
    item_description = input("Enter item description: ")
    item_rental_price = input("Enter item rental price: ")

    # Get price from the market prices module
    item_price = get_market_price(item_code)

    is_furniture = input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        item_material = input("Enter item material: ")
        item_size = input("Enter item size (S,M,L,XL): ")
        new_furniture_item(item_code, item_description, item_price,
                           item_rental_price, item_material, item_size)
    else:
        is_electric_appliance = input("Is this item an electric appliance? (Y/N): ")
        if is_electric_appliance.lower() == "y":
            item_brand = input("Enter item brand: ")
            item_voltage = input("Enter item voltage: ")
            new_electric_appliance_item(item_code, item_description, item_price,
                                        item_rental_price, item_brand, item_voltage)

        else:
            new_inventory_item(item_code, item_description, item_price,
                               item_rental_price)

    FULL_INVENTORY[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")


def new_inventory_item(item_code, item_description, item_price,
                       item_rental_price):
    """
    Function to add a new inventory item to dictionary
    """
    new_item = Inventory(item_code, item_description, item_price,
                         item_rental_price)
    return new_item


def new_furniture_item(item_code, item_description, item_price,
                       item_rental_price, item_material, item_size):
    """
    Function to add a new furniture item to dictionary
    """
    new_item = Furniture(item_code, item_description, item_price,
                         item_rental_price, item_material, item_size)
    return new_item


def new_electric_appliance_item(item_code, item_description, item_price,
                                item_rental_price, item_brand, item_voltage):
    """
    Function to add a new electric appliance item to dictionary
    """
    new_item = ElectricAppliances(item_code, item_description, item_price,
                                  item_rental_price, item_brand, item_voltage)
    return new_item


def item_info():
    """
    Function to print the item information
    """
    item_code = input("Enter item code: ")
    if item_code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[item_code]
        for dict_key, dict_val in print_dict.items():
            print("{}:{}".format(dict_key, dict_val))
    else:
        print("Item not found in inventory")


def exit_program():
    """
    Function to exit program
    """
    sys.exit()

if __name__ == '__main__':
    FULL_INVENTORY = {}
    while True:
        print(FULL_INVENTORY)
        main_menu()()
        input("Press Enter to continue...........")
