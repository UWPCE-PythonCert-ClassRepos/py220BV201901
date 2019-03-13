# Timing results of single vs. multi-thread operations

## Introduction

For assignment 7, we were asked to refactor the previous assignment, and add
multithreading for each table/document to see what the difference would be. I
will summarize the times in a table in a moment. The bottom line is that I did
not see a significant difference in time between serial (linear) and parallel
database ingest.

## Implementation details

The serial (linear) version of the ingest was relatively easy to implement as
all I had to do was add instrumentation and return it as a tuple as documented
in the assignment. I added the table/document name as the first member of the
returned tuple, because it was required for the parallel implementation, and I
thought it was good to be consistent.

## Additions to Parallel implementation

For the parallel implementation, there were two needed additions: locking and
queueing of return values from the threads.

The locking was necessary because I have used a zip file to contain all three
CSV files and reduce their size, so that it can be checked into github along
with the code. This requires the CSV files to be uncompressed from the single
zip file, which is a shared resource. If you look at the runtime logging below,
you can see the locking process. The customer thread gets the lock right away,
but then product and rentals have to wait while customer gets it's CSV file
from the zip archive, and releases the lock. The entire process only adds
approximately 20 msec to the runtime (I guess the SSD in my Mac is fast,
or the file has been cached), and is not included in the measurements.

As can be seen from the logging, the locking works as it should,
serializing access to the zip file. This is a good example of how straight-
forward locking is when working with threads.

While the serial (linear) version can return the required tuples directly,
we don't have the same convenience with threads. The Queue class provides
a straightforward solution here as well, with the addition of a bit of
runtime to push the results onto the queue, and pop them off the queue
when we are done. Queues are implicitly thread-friendly because the
producer of data is adding to the head of the queue, while the consumer
is taking from the tail. I have added a convenience method for the
parallel module to pop the results from the queue.

In addition to the locking added to the zipfile extraction, I added
wrappers for the threads to wrap the customer, product, and rental ingest
methods so that they would have the right signature (*args, **kwargs),
and also provided a handy way to package and put the return values onto
the queue for later retrieval. This allows the existing methods to stay
unchanged.

## Results

Below are the results of a sample run from the command line. It is not the
first run, so it is possible that some of the files have been cached by the
operating system, lending to a reduction of time.

| Method        | Document      | Time (sec) |
| ------------- | ------------- | ---------- |
| Linear        | Customer      |  5.7499    |
|               | Product       |  5.5212    |
|               | Rental        |  4.6694    |
| Parallel      | Customer      | *12.7619*  |
|               | Product       | *13.5816*  |
|               | Rental        | *13.1226*  |
|               |               |            |

To read this table properly,
you have to add up the serial (linear) times, and take the largest parallel
time. As it happens, the parallel threads all finish more or less at the same time
(within a second or two).

__The sum of the serial times is 15.9406 seconds. The longest parallel thread runtime
is 13.5816 seconds__, so there is a bit of speedup with the parallel implementation
despite the extra overhead, but it is not much, and probably not worth the extra
effort and complexity of parallelization in this example. What accounts for the
results not being that dissimilar?

## Analysis

The operation of database ingest is using a lot of library functionality,
including monoengine, which talks to the local database via sockets (probably
UDP). Add to this the File I/O to read the data from each file, and you
have a fair amount of system level overhead that probably is doing it's own
locking in order to be thread-safe.

The context manager for monoengine was expanded to encompass reading the entire
file in this implementation, which is probably optimal as the same socket can
be used to populate the entire document.

```python
    with Connection():
        while True:
            try:
                data = next(import_generator)
                if len(data) != 6:
                    logger.error(f'Data item count: {len(data)}')
                    continue
                # extract items from list and add document to database
                rental = Rental(
                    product_id=data[RENTAL_PROD_ID],
                    user_id=data[RENTAL_USER_ID]
                )
                rental.save()       # This will perform an insert
                record_count += 1
            except StopIteration:
                break
```

There may be significant or trivial
overhead to the document.save() method, especially if there is locking that
needs to be done on the server side. I am assuming that they are using UDP
protocol for networking, which is probably optimal.

The serialization of the unarchival process, while contributing not a lot of
time, forces the parallel implementation to operate serially and peform locking.

## Runtime log

```
Tims-MacBook-Pro:assignment timm$ ./do_csv_import.sh
Ingest CSV files into database...
2019-03-11 18:30:43.981 | INFO     | __main__:main:22 - Start linear ingest from CSV files
2019-03-11 18:30:43.981 | INFO     | linear:linear:24 - Drop all documents
2019-03-11 18:30:49.775 | ERROR    | ingest_csv:ingest_customer_csv:116 - Data item count: 1
2019-03-11 18:30:49.775 | ERROR    | ingest_csv:ingest_customer_csv:116 - Data item count: 1
2019-03-11 18:30:55.002 | ERROR    | ingest_csv:ingest_product_csv:162 - Data item count: 1
2019-03-11 18:30:55.002 | ERROR    | ingest_csv:ingest_product_csv:162 - Data item count: 1
2019-03-11 18:30:59.672 | ERROR    | ingest_csv:ingest_rental_csv:204 - Data item count: 1
2019-03-11 18:30:59.672 | ERROR    | ingest_csv:ingest_rental_csv:204 - Data item count: 1
2019-03-11 18:30:59.672 | INFO     | __main__:main:26 - Start parallel ingest from CSV files
2019-03-11 18:30:59.673 | INFO     | parallel:parallel:28 - Drop all documents
2019-03-11 18:31:00.078 | INFO     | ingest_csv:extract_csv:59 - Acquiring lock for customers.csv
2019-03-11 18:31:00.079 | INFO     | ingest_csv:extract_csv:61 - *** Lock acquired for customers.csv
2019-03-11 18:31:00.080 | INFO     | ingest_csv:extract_csv:59 - Acquiring lock for products.csv
2019-03-11 18:31:00.081 | INFO     | ingest_csv:extract_csv:59 - Acquiring lock for rentals.csv
2019-03-11 18:31:00.087 | INFO     | ingest_csv:extract_csv:65 - Releasing lock for customers.csv
2019-03-11 18:31:00.088 | INFO     | ingest_csv:extract_csv:61 - *** Lock acquired for products.csv
2019-03-11 18:31:00.091 | INFO     | ingest_csv:extract_csv:65 - Releasing lock for products.csv
2019-03-11 18:31:00.091 | INFO     | ingest_csv:extract_csv:61 - *** Lock acquired for rentals.csv
2019-03-11 18:31:00.095 | INFO     | ingest_csv:extract_csv:65 - Releasing lock for rentals.csv
2019-03-11 18:31:12.838 | ERROR    | ingest_csv:ingest_customer_csv:116 - Data item count: 1
2019-03-11 18:31:12.838 | ERROR    | ingest_csv:ingest_customer_csv:116 - Data item count: 1
2019-03-11 18:31:13.202 | ERROR    | ingest_csv:ingest_rental_csv:204 - Data item count: 1
2019-03-11 18:31:13.202 | ERROR    | ingest_csv:ingest_rental_csv:204 - Data item count: 1
2019-03-11 18:31:13.661 | ERROR    | ingest_csv:ingest_product_csv:162 - Data item count: 1
2019-03-11 18:31:13.661 | ERROR    | ingest_csv:ingest_product_csv:162 - Data item count: 1
2019-03-11 18:31:13.662 | INFO     | __main__:main:30 - CSV ingest completed
Linear ingest statistics:
customer doc: num  records: 9999
customer doc: time elapsed: 5.749906344
product doc: num  records: 9999
product doc: time elapsed: 5.521199267999999
rental doc: num  records: 9999
rental doc: time elapsed: 4.669459174
Parallel ingest statistics:
customer doc: num  records: 9999
customer doc: time elapsed: 12.761913809
rental doc: num  records: 9999
rental doc: time elapsed: 13.122601850999999
product doc: num  records: 9999
product doc: time elapsed: 13.581593243
```