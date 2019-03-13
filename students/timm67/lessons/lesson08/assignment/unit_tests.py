from inventory import add_furniture
from inventory import single_customer

def test_add_furniture():
    add_furniture("invoice01.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    add_furniture("invoice01.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    add_furniture("invoice01.csv", "Alex Gonzales", "Queen Mattress", 17)

def test_single_customer():
    create_invoice = single_customer("Susan Wong", "SW_invoice.csv")
    create_invoice("test_items.csv")
