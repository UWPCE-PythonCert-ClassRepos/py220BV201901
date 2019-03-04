#!/bin/sh
export PYTHONPATH=.
python3 -m pylint ./database.py
python3 -m pylint ./ingest_csv.py
python3 -m pylint ./models.py
# python3 -m coverage run --source=./basic_operations.py k -m pytest tests/test_unit.py; 
pytest ./tests/test_unit.py
