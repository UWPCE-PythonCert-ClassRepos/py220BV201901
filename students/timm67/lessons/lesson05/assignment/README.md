NOTES:

- There are two shell scripts that run both the ingest of the provided CSV file into database,
and run the pylint/unit tests.

- The provided CSV file was converted with the following command to remove any unicode characters:

```iconv -f utf-8 -t utf-8 -c customer.csv > customer2.csv```

- The cleaned CSV file has been put into a zip file and is automatically extracted from the
archive at runtime

- To run the unit tests, pylinting, execute the `do_unit_tests.sh` script

- To run the CSV extract and database ingest function with generator functionality, execute the `do_csv_import.sh` script