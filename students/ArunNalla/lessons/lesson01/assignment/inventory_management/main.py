# Launches the user interface for the inventory management system
""" functional code to manage the items infos"""
import sys
from collections import defaultdict
import market_prices
import inventory_class as ic
import furniture_class as fc
import electric_appliances_class as eac

FULL_INVENTORY = defaultdict(dict)

def main_menu(user_prompt=None):
    """ User input upon enter of the site with some guidelines what to do"""
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (', {}' * (len(options)-1))).format(*options)
        print("Please choose from the following options {}".format(options_str))
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)

def get_price(item_code):
    """ Docstring to get the price of the item"""
    print("Get price {}".format(item_code))


def add_new_item():
    """function for adding new items to the inventory"""
    global FULL_INVENTORY
    item_code = input("Enter item code: ")
    item_description = input("Enter item description: ")
    item_rental_price = input("Enter item rental price: ")

    # Get price from the market prices module
    item_price = market_prices.get_latest_price(item_rental_price)

    is_furniture = input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        item_material = input("Enter item material: ")
        item_size = input("Enter item size (S,M,L,XL): ")
        new_item = fc.Furniture(item_code, item_description, item_price,
                                item_rental_price,
                                item_material, item_size)
    else:
        is_electric_appliance = input("Is this item an electric "
                                      "appliance? (Y/N): ")
        if is_electric_appliance.lower() == "y":
            item_brand = input("Enter item brand: ")
            item_voltage = input("Enter item voltage: ")
            new_item = eac.ElectricAppliances(item_code, item_description,
                                              item_price, item_rental_price,
                                              item_brand, item_voltage)
        else:
            new_item = ic.Inventory(item_code, item_description, item_price,
                                    item_rental_price)
    FULL_INVENTORY[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")
    return FULL_INVENTORY


def item_info():
    """Code to get the details of each item"""
    item_code = input("Enter item code: ")
    if item_code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[item_code]
        for keys, values in print_dict.items():
            print("{}:{}".format(keys, values))
    else:
        print("Item not found in inventory")

def exit_program():
    """Code to exit out of the program"""
    sys.exit()

if __name__ == '__main__':

    while True:
        print(dict(FULL_INVENTORY))
        main_menu()()
        input("Press Enter to continue...........")
