# Launches the user interface for the inventory management system
"""
This is the main program/module for the inventory managment system.
"""
import sys
# from inventory_class import Inventory
# from furniture_class import Furniture
# from market_prices import get_latest_price
# from electric_appliances_class import ElectricAppliances

#USING this to see:  NOT working
#ModuleNotFoundError: __path__ attribute not found on 'inventory_management.main
from .market_prices import get_latest_price
from .inventory_class import Inventory
from .furniture_class import Furniture
from .electric_appliances_class import ElectricAppliances

FULL_INVENTORY = {}

def main_menu(user_prompt=None):
    """
    This is the main menu.
    """
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print("Please choose from the following options"
              " ({}):".format(options_str))
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)

def get_price(item_code):
    """
    What does this do?
    """
    print("Get price {}".format(item_code))

def add_new_item():
    """
    What does this do?
    """
    #global FULL_INVENTORY
    item_code = input("Enter item code: ")
    item_description = input("Enter item description: ")
    item_rent_price = input("Enter item rental price: ")

    # Get price from the market prices module
    item_price = get_latest_price(item_code)

    is_funiture = input("Is this item a piece of furniture? (Y/N): ")
    if is_funiture.lower() == "y":
        item_material = input("Enter item material: ")
        item_size = input("Enter item size (S,M,L,XL): ")
        new_item = Furniture(item_code, item_description, item_price,
                             item_rent_price, item_material, item_size)
    else:
        is_electric_appliance = input("Is this item an electric"
                                      "appliance? (Y/N): ")
        if is_electric_appliance.lower() == "y":
            item_brand = input("Enter item brand: ")
            item_voltage = input("Enter item voltage: ")
            new_item = ElectricAppliances(
                item_code, item_description,
                item_price, item_rent_price,
                item_brand, item_voltage)
        else:
            new_item = Inventory(item_code, item_description,
                                 item_price, item_rent_price)

    FULL_INVENTORY[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")


def item_info():
    """
    What does this do?
    """
    item_code = input("Enter item code: ")
    if item_code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[item_code]
        for key, value in print_dict.items():
            print("{}:{}".format(key, value))
    else:
        print("Item not found in inventory")

def exit_program():
    """
    What does this do?
    """
    sys.exit()

if __name__ == '__main__':
    FULL_INVENTORY = {}
    while True:
        print(FULL_INVENTORY)
        main_menu()()
        input("Press Enter to continue...........")
