import unittest
import pandas as pd  
import random

from SE_Assignment import Customer
from SE_Assignment import Product
from SE_Assignment import SalesPerson
from SE_Assignment import Warehouse

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

class TestProductMethods(unittest.TestCase):


    def test_to_get_customer_details__positive_testing(self):
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

    def test_to_get_customer_details__negative_testing(self):
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


class TestSalesPersonMethods(unittest.TestCase):


    def test_to_get_customer_details__positive_testing(self):
        sp = SalesPerson()
        sales_person_id = 1001
        sales_percentage = 10
        response_data = [1001, 10]

        self.assertEqual(list(SalesPerson.addSalesCommission(sales_person_id, sales_percentage))[:-1],response_data)

    def test_to_get_customer_details__negative_testing(self):
        sp = SalesPerson()
        sales_person_id = 1002
        sales_percentage = 10
        response_data = [1001, 10]

        self.assertEqual(SalesPerson.addSalesCommission(sales_person_id, sales_percentage),'Enter valid customer ID')

class TestWarehouseMethods(unittest.TestCase):

    # def test_lookup_Products_Under_A_Brand__positive_testing(self):
    #     w = Warehouse()
    #     w.lookupProductsUnderABrand(brand_name)


    #     self.assertEqual(list(SalesPerson.addSalesCommission(sales_person_id, sales_percentage))[:-1],response_data)

    def test_lookup_Products_InAWarehouse__positive_testing(self):
        w = Warehouse()
        warehouse_id = 1
        response_data = {'product_name': {0: 'Samsung QN900A Neo QLED 8K',
          3: 'Sony A90J OLED',
          4: 'Sony Bravia X90J',
          5: 'TCL 6-Series with Mini LED',
          6: 'Vizio H-1 OLED TV',
          9: 'Samsung The Frame (2021)',
          11: 'Bose Wave SoundTouch Music System',
          13: 'PHILIPS Bluetooth Stereo System'},
         'brand': {0: 'Samsung',
          3: 'Sony',
          4: 'Sony',
          5: 'TCL',
          6: 'Vizio',
          9: 'Samsung',
          11: 'Bose',
          13: 'Philips'},
         'warehouse': {0: 'w1',
          3: 'w1',
          4: 'w1',
          5: 'w1',
          6: 'w1',
          9: 'w1',
          11: 'w1',
          13: 'w1'},
         'selling_cost': {0: '$200',
          3: '$200',
          4: '$200',
          5: '$200',
          6: '$200',
          9: '$200',
          11: '$200',
          13: '$200'},
         'reviews': {0: 5.0, 3: 4.5, 4: 4.7, 5: 4.1, 6: 3.8, 9: 4.8, 11: 4.3, 13: 3.9},
         'cost_price': {0: '$300',
          3: '$300',
          4: '$300',
          5: '$300',
          6: '$300',
          9: '$300',
          11: '$300',
          13: '$300'},
         'quantity': {0: 51, 3: 0, 4: 66, 5: 0, 6: 15, 9: 28, 11: 33, 13: 40},
         'category': {0: 'TV',
          3: 'TV',
          4: 'TV',
          5: 'TV',
          6: 'TV',
          9: 'TV',
          11: 'Sterio',
          13: 'Sterio'},
         'location': {0: 'Aisle L1',
          3: 'Aisle K5',
          4: 'Aisle K9',
          5: 'Aisle K4',
          6: 'Aisle J19',
          9: 'Aisle J11',
          11: 'Aisle N1',
          13: 'Aisle M13'}}
        self.assertEqual(w.lookupProductsInAWarehouse(warehouse_id).to_dict(),response_data)

    def test_lookup_Products_InAWarehouse__negative_testing(self):
        w = Warehouse()
        warehouse_id = 10
        response_data = "warehouse ID unavailable!"

        self.assertEqual(w.lookupProductsInAWarehouse(warehouse_id),response_data)

    def test_lookupProductsUnderABrand__positive_testing(self):
        w = Warehouse()
        brand_name = "LG"
        response_data = {'product_name': {1: 'LG G1 Gallery Series OLED', 2: 'LG C1 Series OLED TV'},
         'brand': {1: 'LG', 2: 'LG'},
         'warehouse': {1: 'w2', 2: 'w2'},
         'selling_cost': {1: '$200', 2: '$200'},
         'reviews': {1: 3.7, 2: 5.0},
         'cost_price': {1: '$300', 2: '$300'},
         'quantity': {1: 0, 2: 72},
         'category': {1: 'TV', 2: 'TV'},
         'location': {1: 'Aisle K14', 2: 'Aisle K11'}}

        self.assertEqual(w.lookupProductsUnderABrand(brand_name).to_dict(),response_data)

    def test_lookupProductsUnderABrand__negative_testing(self):
        w = Warehouse()
        brand_name = "One Plus"
        response_data = "Product unavailable !"

        self.assertEqual(w.lookupProductsUnderABrand(brand_name),response_data)

if __name__ == '__main__':
    unittest.main()
