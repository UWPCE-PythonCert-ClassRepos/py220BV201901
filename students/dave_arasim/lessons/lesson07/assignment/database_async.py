""""
MongoDB database model for Lesson 7 - parallel processing (imports database.py)
"""

import os
import asyncio
from datetime import datetime
import database as l

program_start = datetime.now()

data_dir = os.path.dirname(os.path.abspath(__file__))

loop = asyncio.get_event_loop()

tasks = [  
    asyncio.ensure_future(l.import_products_async(data_dir, "products.csv")),
    asyncio.ensure_future(l.import_customers_async(data_dir, "customers.csv")),
    asyncio.ensure_future(l.import_rentals_async(data_dir, "rentals.csv"))
]

loop.run_until_complete(asyncio.wait(tasks))
loop.close()

program_finish = datetime.now()
program_elapsed = (program_finish - program_start).total_seconds()
print(f'Elapsed program time: {program_elapsed}')
