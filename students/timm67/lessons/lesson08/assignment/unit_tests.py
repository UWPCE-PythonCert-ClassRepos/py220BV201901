from inventory import *
add_furniture("invoice01.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
add_furniture("invoice01.csv", "Edward Data", "KT78", "Kitchen Table", 10)
add_furniture("invoice01.csv", "Alex Gonzales", "Queen Mattress", 17)

create_invoice = single_customer("Susan Wong", "SW_invoice.csv")
create_invoice("test_items.csv")
