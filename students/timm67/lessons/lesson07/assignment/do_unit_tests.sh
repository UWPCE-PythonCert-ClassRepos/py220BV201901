#!/bin/sh
export PYTHONPATH=.
pylint --py3k ./database.py
pylint --py3k ./ingest_csv.py
pylint --py3k ./models.py
pylint --py3k ./linear.py
pylint --py3k ./parallel.py

# python3 -m coverage run --source=./basic_operations.py k -m pytest tests/test_unit.py; 
# pytest ./tests/unit_tests.py
