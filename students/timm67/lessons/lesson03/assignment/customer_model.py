from peewee import Model
from peewee import CharField
from peewee import IntegerField
from peewee import BooleanField
from peewee import DecimalField
from peewee import SqliteDatabase


database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite


class BaseModel(Model):
    class Meta:
        database = database


class Customer(BaseModel):
    """
    Customer model to store basic information such as name, address, 
    phone number, email, customer status, and credit limit
    """
    customer_id = IntegerField(unique=True, primary_key=True)
    name = CharField(max_length=30)
    lastname = CharField(max_length=30)
    home_address = CharField(max_length=60)
    phone_number = CharField(max_length=20)
    email_address = CharField(max_length=60)
    status = BooleanField()
    credit_limit = DecimalField(max_digits=7, decimal_places=2)


database.create_tables([
    Customer
    ])

database.close()
