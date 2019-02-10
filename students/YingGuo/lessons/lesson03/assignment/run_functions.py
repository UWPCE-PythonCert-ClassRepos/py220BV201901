from lesson03.assignment.basic_operations import *

with open ("customer.csv", 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, dialect='excel', quotechar='|')
        for row in csv_reader:
            print(', '.join(row))
