import os
import asyncio
import time  
from datetime import datetime
import database_async_def as l

async def say(what, when):
    await asyncio.sleep(when)
    print(what)

async def stop_after(loop, when):
    await asyncio.sleep(when)
    loop.stop()

data_dir = os.path.dirname(os.path.abspath(__file__))

loop = asyncio.get_event_loop()

#loop.create_task(l.import_products_data(data_dir, "products.csv"))
#loop.create_task(l.import_customers_data(data_dir, "customers.csv"))
#loop.create_task(l.import_rentals_data(data_dir, "rentals.csv"))
#loop.create_task(stop_after(loop, 25)) DKA

#loop.run_forever() DKA

tasks = [  
    asyncio.ensure_future(l.import_products_data(data_dir, "products.csv")),
    asyncio.ensure_future(l.import_customers_data(data_dir, "customers.csv")),
    asyncio.ensure_future(l.import_rentals_data(data_dir, "rentals.csv"))
]

loop.run_until_complete(asyncio.wait(tasks)) # DKA
loop.close()

# Andy to offer way to do loop.stop() without having a timeout stop_after()
