#!/bin/sh
python3 -m pylint ./inventory_management
python3 -m coverage run --source=inventory_management -m unittest tests/test_unit.py; python3 -m coverage report
