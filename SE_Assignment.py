import pandas as pd
from csv import writer
from datetime import datetime
import random

class Product:

    def __init__(self):
        self.products = pd.read_csv (r'product_ASE.csv')
    
    def getProductInfo(self, product_id):
        self.products.reset_index(inplace=True)
        self.products = self.products.rename(columns = {'index':'id'})
        
        final_product_set = self.products[self.products['id'] == product_id]
        return final_product_set
        
    def update_product_quantity(self, product_id):
        self.products.loc[product_id, 'quantity'] = self.products.at[product_id, 'quantity'] - 1
        self.products.to_csv("product_ASE.csv", index=False)


class Customer:
    
    def __init__(self):
        self.customers = pd.read_csv (r'customer_ASE.csv')
        self.sales_tax = self.customers.sale_percentage
        
    def createCustomer(self,phone_number, customer_details):
        List = [customer_details[0], phone_number, customer_details[1],"customer",round(random.uniform(0, 5),1)]
        with open('customer_ASE.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(List)
            f_object.close()
        
    def getCustomerDetails(self,phone_number):
        self.customers.reset_index(inplace=True)
        customer = self.customers.rename(columns = {'index':'id'})
        val = self.customers[self.customers['phone_number']==int(phone_number)] 
        return val 

        
class invoice(Product):

    def __init__(self):
        self.invoice = pd.read_csv (r'invoice_ASE.csv')
        self.invoice.reset_index(inplace=True)
        self.invoice = self.invoice.rename(columns = {'index':'id'})
        
    def createInvoice(self,product_id, mode_of_payment, customer_phone_number, shipment_type):
        c = Customer()
        customer = c.getCustomerDetails(customer_phone_number)
        date_time_value = datetime.now()
        List = [customer.index.values[0],mode_of_payment,date_time_value,shipment_type]

        with open('invoice_ASE.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(List)
            f_object.close()
        
        newly_created_invoice_id = self.invoice.tail(1).id.values[0]
        
        p = Product()
        ph = PurchaseHistory()
        for product_id_value in product_id:
            ph.addPurchasedProducts(newly_created_invoice_id,product_id_value,customer_phone_number)
            
            #CALL TO UPDATE PRODUCT QUANTITY
            p.update_product_quantity(product_id_value)
        
        return self.invoice.tail(1).id.values[0]


class PurchaseHistory:
    
    def __init__(self):
        self.purchaseHistory = pd.read_csv (r'purchase_history_ASE.csv')
        
    def addPurchasedProducts(self, invoice_id, product_id,customer_phone_number):
        Row_value_to_be_inserted = [invoice_id,product_id,customer_phone_number]
        with open('purchase_history_ASE.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(Row_value_to_be_inserted)
            f_object.close()
            
class Warehouse(Product):
    
    def inventoryLookup(self,warehouse_id, product_id, brand):
        
        # IF THE USER WANTS TO GET TO KNOW DETAILS OF A PARTICULAR PRODUCT
        if product_id:
            product_detail = p.getProductInfo(product_id)
            print("Details of the Product with product_id : " + str(product_id))
            print("===========================================")
            print(product_detail.to_string(index=False))
            print("---------------------------------------------------------------------------------------")
        
        # IF THE USER WANTS TO GET THE CURRENT AVAILABLITY OF A PARTICULAR BRAND
        if brand:
            val = self.products[self.products['brand']== brand]
            print("Products under the brand : "+brand)
            print("===============================")
            print(val.to_string(index=False))  
            print("---------------------------------------------------------------------------------------")
            
        # IF THE USER WANTS TO SEE ALL PRODUCTS THAT ARE IN A PARTICULAR WAREHOUSE
        if warehouse_id:
            val = self.products[self.products['warehouse']== "w" + str(warehouse_id)]
            print("Products under the warehouse : w"+str(warehouse_id))
            print("===============================")
            print(val.to_string(index=False))
    
class SalesPerson:
    def addSalesCommission(sales_person_id, commission_value):
        Row_value_to_be_inserted = [sales_person_id,commission_value,datetime.now()]
        with open('sales_commission.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(Row_value_to_be_inserted)
            f_object.close()

def main():

    print("What would you like to do? Please select one of the following:")
    print("1. Place an order")
    print("2. Inventory Lookup")
    val = input()
    if val == "1":
        customer_phone_number = input("Enter customer's phone number : ")
        c = Customer()
        customer = c.getCustomerDetails(customer_phone_number)
        if customer.empty:
            print("OOPS! Unfortunately the database don't have any details about this customer! Please provide the following details to place an order. Thank you!")
            name = input("Enter the customer name ")
            address = input("Enter the customer address ")
            c.createCustomer(customer_phone_number,[name,address,"customer"])
            
        list_of_products_to_be_purchased = []
        condition_to_stop_product_addition = 'Yes'
        while condition_to_stop_product_addition == "Yes":
            product_id = input("Enter the product ID: ")
            list_of_products_to_be_purchased.append(int(product_id))
            condition_to_stop_product_addition = input("do you want to add more products to the purchase list ? Yes / No? \n ")
            if condition_to_stop_product_addition != "Yes":
                break
            
        i = invoice()
        c = Customer()
    
        salesperson_during_purchase = int(input("ID of the sales person : "))
        mode_of_payment = input("How would the customer like to make the payment ? Cash / Card ? ")
        shipment_type = input("Is it a home delivery order or a take-away order ? ")
        
        delivery_fee = 0
        if shipment_type.lower() in "home delivery":
            delivery_fee += 5
            
        print("==============================================")
        print("LIST OF PRODUCTS ADDED TO THE CART :")
        print("==============================================")
        purchase_value = 0
        
        for product_id in list_of_products_to_be_purchased:
            p = Product()
            product_item = p.getProductInfo(product_id)
            purchase_value += int(product_item.selling_cost.values[0][1:])
            print((product_item.product_name.to_string(index=False).ljust(40) + product_item.selling_cost.to_string(index=False)).expandtabs(30))
        if delivery_fee > 0: 
            print("Delivery fee".ljust(40)+"$"+str(delivery_fee))
            purchase_value += 5
        sales_tax_value = purchase_value * ((c.customers[c.customers['phone_number']==int(customer_phone_number)].sale_percentage.values[0])/100)
        print("----------------------------------------------")
        print("Purchase Value".ljust(40)+"$"+str(purchase_value))
        print("Sales tax".ljust(40)+"$"+str(sales_tax_value))
        total_purchase_value = purchase_value + sales_tax_value
        print("----------------------------------------------")
        print("Total Purchase Value".ljust(40)+"$"+str(total_purchase_value))
        print("----------------------------------------------")
        
        permission_to_proceed = input("do you want to proceed ?")
        if permission_to_proceed.lower() == "yes":
            latest_invoice_id = i.createInvoice(list_of_products_to_be_purchased, mode_of_payment, customer_phone_number, shipment_type)
            print("The order has been placed with invoice ID : "+str(latest_invoice_id))
            print("==============================================")
            print("INVOICE :".ljust(40)+"#"+str(latest_invoice_id))
            print("==============================================")
            print("Customer details :")
            print("Name".ljust(20)+customer.name.values[0])
            print("Phone Number".ljust(20)+customer_phone_number)
            print("Address".ljust(20)+c.customers[c.customers['phone_number']==int(customer_phone_number)].address.values[0])
            print("==============================================")
            print("Purchased Products :")
            print("==============================================")
            purchase_value = 0

            for product_id in list_of_products_to_be_purchased:
                p = Product()
                product_item = p.getProductInfo(product_id)
                purchase_value += int(product_item.selling_cost.values[0][1:])
                print((product_item.product_name.to_string(index=False).ljust(40) + product_item.selling_cost.to_string(index=False)).expandtabs(30))
            if delivery_fee > 0: 
                print("Delivery fee".ljust(40)+"$"+str(delivery_fee))
                purchase_value += 5
            sales_tax_value = purchase_value * ((c.customers[c.customers['phone_number']==int(customer_phone_number)].sale_percentage.values[0])/100)
            print("----------------------------------------------")
            print("Purchase Value".ljust(40)+"$"+str(purchase_value))
            print("Sales tax".ljust(40)+"$"+str(sales_tax_value))
            total_purchase_value = purchase_value + sales_tax_value
            print("----------------------------------------------")
            print("Total Purchase Value".ljust(40)+"$"+str(total_purchase_value))
            print("----------------------------------------------")
            SalesPerson.addSalesCommission(latest_invoice_id, total_purchase_value * (round(random.uniform(5, 10),2)/100)) 
            
        else:
            print("Purchase Aborted ! Thank you!")
            return
        
    elif val == "2":
        p = Product()
        print("==============================================")
        print("Inventory LookUp Options : ")
        print("==============================================")
        print("1. Check for a product availability")
        print("2. Check for products that are to be restocked")
        print("3. Check for product location in Warehouse")
        print("4. Check for product details")
        print("5. Pull up products based on rating value")
        print("6. Pull up products based on selling cost")
        
        print("----------------------------------------------")
        lookup_option = int(input("Your Lookup option : "))
        if lookup_option == 1:
            product_id = int(input("Please enter the product ID :"))
            product_details = p.getProductInfo(product_id)
            print("Information Result :")
            print("--------------------")
            print(product_details.loc[:, ~product_details.columns.isin(['id', 'cost_price', 'category'])].to_string(index=False))
#         elif lookup_option == 2:
            
#             product_set = p[p['quantity']<5] 
#         elif lookup_option == 3:
            
#         elif lookup_option == 4:
        else:
            print("oops, you didnt enter any option. Try again Later!")
        
    
    
if __name__ == "__main__":
    main()