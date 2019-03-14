add_furniture method implemented that simply creates or appends an invoice file.
File is created using the argument provided to the add_furniture method.

single_customer method created that takes two arguments, customer name and invoice file name.
The single_customer method wraps another method called consumerentalitems.

consumerentalitems takes one argument, rental items file name.

consumerentalitems uses the two arguments from the wrapping function and the rental items file
to create a new invoice file for just the single customer.
single_customer returns the consumerentalitem function.