from peewee import Model
from peewee import CharField
from peewee import BooleanField
from peewee import DecimalField
from peewee import ForeignKeyField
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
    customer_id = CharField(max_length=20, unique=True, primary_key=True)
    name = CharField(max_length=30)
    lastname = CharField(max_length=30)
    phone_info = CharField(max_length=30)
    home_address = CharField(max_length=60)
    email_address = CharField(max_length=60)
    status = BooleanField()
    credit_limit = DecimalField(max_digits=7, decimal_places=2)


class PhoneInfo(BaseModel):
    """
    Separate table to accumulate possibly disparate contact info.
    info_supplied is overall string that is parsed to break out
    individual fields.
    """

    country_code = CharField(max_length=3, null=True)
    area_code = CharField(max_length=3, null=True)
    phone_number = CharField(max_length=8, null=True)
    extension = CharField(max_length=8, null=True)
    description = CharField(max_length=8, null=True)
    customer = ForeignKeyField(Customer, backref='has_phone_info', null=False)


database.create_tables([
    Customer,
    PhoneInfo
    ])

database.close()
