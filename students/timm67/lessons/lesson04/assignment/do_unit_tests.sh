#!/bin/sh
export PYTHONPATH=.
# remove customers.db in case import_db was executed first
rm -f customers.db
python3 -m pylint ./basic_operations.py
python3 -m pylint ./ingest_csv.py
# python3 -m coverage run --source=./basic_operations.py k -m pytest tests/test_unit.py; 
pytest ./tests/test_unit.py
