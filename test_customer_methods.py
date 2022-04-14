import unittest
import pandas as pd  
import random

from SE_Assignment import Customer

class TestCustomerMethods(unittest.TestCase):

    def test_for_phone_number_negative_testing(self):
        customer_phone_number = "6666"
        c = Customer()
        self.assertEqual(c.hasValidPhonenumber(customer_phone_number), False)

    def test_for_phone_number_positive_testing(self):
        customer_phone_number = "5622537022"
        c = Customer()
        self.assertEqual(c.hasValidPhonenumber(customer_phone_number), True)

    def test_to_get_customer_details_positive_testing(self):
        customer_phone_number = "5622537022"
        response_data = {'index': {16: 16},
         'name': {16: 'Shruthi Venkatachalam 1'},
         'phone_number': {16: 5622537022},
         'address': {16: '123 Ave, Long Beach, CA'},
         'role': {16: 'customer'},
         'sale_percentage': {16: 3.0}}

        c = Customer()
        self.assertEqual(c.getCustomerDetails("5622537022").to_dict(), response_data)


if __name__ == '__main__':
    unittest.main()
