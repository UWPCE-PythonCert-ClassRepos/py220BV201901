"""
    Lesson05 tests
    HP Norton products in MongoDB

"""

import lesson05.assignment.hpnorton_products.database as mongo


def test_import_date():
    """ import data """

    result = mongo.import_data('c:/Users/motia/OneDrive/Documents/PythonCertClass/py220BV201901/students/Shawn_DeGraw/lessons/lesson05/assignment', 'products.csv', 'customers.csv', 'rentals.csv')

    assert result == [(10, 10, 9), (0, 0, 0)]


def test_show_avail_products():
    """ test for available products """

    result = mongo.show_available_products()
    assert result == {
                        'prd001':
                        {
                            'description':'60-inch TV stand',
                            'product_type':'livingroom',
                            'quantity_available':'3'
                        },
                        'prd003':
                        {
                            'description':'Acacia kitchen table',
                            'product_type':'kitchen',
                            'quantity_available':'7'
                        },
                        'prd004':
                        {
                            'description':'Queen bed',
                            'product_type':'bedroom',
                            'quantity_available':'10'
                        },
                        'prd005':
                        {
                            'description':'Reading lamp',
                            'product_type':'bedroom',
                            'quantity_available':'20'
                        },
                        'prd006':
                        {
                            'description':'Portable heater',
                            'product_type':'bathroom',
                            'quantity_available':'14'
                        },
                        'prd008':
                        {
                            'description':'Smart microwave',
                            'product_type':'kitchen',
                            'quantity_available':'30'
                        },
                        'prd010':
                        {
                            'description':'60-inch TV',
                            'product_type':'livingroom',
                            'quantity_available':'3'
                        }}


def test_show_rentals():
    """ test for available products """

    result = mongo.show_rentals('prd002')

    assert result == {
        'user005':
            {
                'name':'Dan Sounders',
                'address':'861 Honeysuckle Lane',
                'phone_number':'206-279-1723',
                'email':'soundersoccer@mls.com'
            },
        'user008':
            {
                'name':'Shirlene Harris',
                'address':'4329 Honeysuckle Lane',
                'phone_number':'206-279-5340',
                'email':'harrisfamily@gmail.com'
            }
        }
