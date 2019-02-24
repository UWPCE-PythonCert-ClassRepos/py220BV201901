#!/bin/sh
export PYTHONPATH=.
echo 'Removing existing customers.db file...'
rm -f ./customers.db
echo 'Removing existing customer.csv file...'
rm -f ./customer.csv
echo 'Uncompress/ingest customer.csv file into database...'
python3 ./main.py
