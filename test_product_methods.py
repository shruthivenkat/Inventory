import unittest
import pandas as pd  
import random

from SE_Assignment import Product

class TestProductMethods(unittest.TestCase):


    def test_to_get_customer_details_positive_testing(self):
        p = Product()

        product_id = 3
        response_data = {'id': {3: 3},
         'product_name': {3: 'Sony A90J OLED'},
         'brand': {3: 'Sony'},
         'warehouse': {3: 'w1'},
         'selling_cost': {3: '$200'},
         'reviews': {3: 4.5},
         'cost_price': {3: '$300'},
         'quantity': {3: 0},
         'category': {3: 'TV'},
         'location': {3: 'Aisle K5'}}

        self.assertEqual(p.getProductInfo(product_id).to_dict(),response_data)

    def test_to_get_customer_details_negative_testing(self):
        p = Product()

        product_id = 300
        response_data = {'id': {},
         'product_name': {},
         'brand': {},
         'warehouse': {},
         'selling_cost': {},
         'reviews': {},
         'cost_price': {},
         'quantity': {},
         'category': {},
         'location': {}}

        self.assertEqual(p.getProductInfo(product_id).to_dict(),response_data)

if __name__ == '__main__':
    unittest.main()
