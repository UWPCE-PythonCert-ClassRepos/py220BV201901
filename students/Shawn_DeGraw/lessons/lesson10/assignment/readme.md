Added a decorator to database.py. The decorator used is very similar to the one used
in the lesson09 decorator portion.

The decorator wraps all of the functions providing execution timing and writing the
data to the timings file. The data written includes the time and function name.

I was not sure how to capture the number of records stored to the database. Perhaps I
would need a refactor to perform that piece.