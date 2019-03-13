#!/bin/sh
export PYTHONPATH=.
pylint --py3k ./inventory.py

# python3 -m coverage run --source=./basic_operations.py k -m pytest tests/test_unit.py; 
pytest ./unit_tests.py
