from inventory import add_furniture
from inventory import single_customer


def main():

    add_furniture("invoice01.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    add_furniture("invoice01.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    add_furniture("invoice01.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17)

    add_items = single_customer('Susan Wong', 'sw_invoice.csv')
    add_items('test_items.csv')

if  __name__ == '__main__':
    main()
