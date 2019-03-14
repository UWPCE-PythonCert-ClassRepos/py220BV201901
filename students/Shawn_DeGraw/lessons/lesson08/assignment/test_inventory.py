"""
    Autograde Lesson 8 assignment

"""


from lesson08.assignment import inventory as l


def test_add_furniture():
    l.add_furniture("invoice01.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    l.add_furniture("invoice01.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    l.add_furniture("invoice01.csv", "Alex Gonzales", "QM67", "Queen Mattress", 17)


    with open('invoice01.csv','r') as testfile:
        assert testfile.readline() == "Elisa Miles, LR04, Leather Sofa, 25\n"
        assert testfile.readline() == "Edward Data, KT78, Kitchen Table, 10\n"
        assert testfile.readline() == "Alex Gonzales, QM67, Queen Mattress, 17\n"

def test_single_customer():
    create_invoice = l.single_customer("Susan Wong", "SW_invoice.csv")
    create_invoice("test_items.csv")

    create_invoice2 = l.single_customer("Jason Jones", "JJ_invoice.csv")
    create_invoice2("test_items.csv")

    with open('SW_invoice.csv','r') as testfile:
        assert testfile.readline() == "Susan Wong, LR04, Leather Sofa, 25.00\n"
        assert testfile.readline() == "Susan Wong, KT78, Kitchen Table, 10.00\n"
        assert testfile.readline() == "Susan Wong, BR02, Queen Mattress, 17.00\n"

    with open('JJ_invoice.csv','r') as testfile:
        assert testfile.readline() == "Jason Jones, LR04, Leather Sofa, 25.00\n"
        assert testfile.readline() == "Jason Jones, KT78, Kitchen Table, 10.00\n"
        assert testfile.readline() == "Jason Jones, BR02, Queen Mattress, 17.00\n"
