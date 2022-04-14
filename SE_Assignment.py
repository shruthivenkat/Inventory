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
        product_quanity = self.products.at[product_id, 'quantity']
        if product_quanity > 1:
            self.products.loc[product_id, 'quantity'] = product_quanity - 1
        else:
            self.products.loc[product_id, 'quantity'] = 0
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
    
    def hasValidPhonenumber(self,customer_phone_number):
        if (len(customer_phone_number)) == 10:
            return True
        else:
            return False

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
    
    def displayInvoice(self,invoice_id,customer,list_of_products_purchased,delivery_fee,sum_paid_at_time_of_purchase,sales_tax_value):
        print("==============================================")
        print("INVOICE :".ljust(40)+"#"+str(invoice_id))
        print("==============================================")
        print("Customer details :")
        print("Name".ljust(20)+customer.name.values[0])
        print("Phone Number".ljust(20)+str(customer.phone_number.values[0]))
        print("Address".ljust(20)+str(customer.address.values[0]))
        print("==============================================")
        print("Purchased Products :")
        print("==============================================")
        purchase_value = 0
        
        for product_id in list_of_products_purchased:
            p = Product()
            product_item = p.getProductInfo(product_id)
            purchase_value += int(product_item.selling_cost.values[0][1:])
            print((product_item.product_name.to_string(index=False).ljust(40) + product_item.selling_cost.to_string(index=False)).expandtabs(30))
        
        if delivery_fee > 0: 
            print("Delivery fee".ljust(40)+"$"+str(delivery_fee))
            purchase_value += delivery_fee

        print("----------------------------------------------")
        print("Purchase Value".ljust(40)+"$"+str(purchase_value))
        print("Sales tax".ljust(40)+"$"+str(sales_tax_value))
        total_purchase_value = purchase_value + sales_tax_value
        print("----------------------------------------------")
        print("Total Purchase Value".ljust(40)+"$"+str(total_purchase_value))
        print("Sum Paid at time of purchase".ljust(40)+"$"+str(sum_paid_at_time_of_purchase))
        print("----------------------------------------------")
        print("Due Amount".ljust(40)+"$"+str(round((total_purchase_value - sum_paid_at_time_of_purchase),2)))
        print("----------------------------------------------")

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
    
    def lookupProductsUnderABrand(self,brand_name):
        products_with_the_give_brand = self.products[self.products['brand']== brand_name]
        print("Products under the brand : "+brand_name)
        print("=======================================================================================")
        print(products_with_the_give_brand.to_string(index=False))  
        print("---------------------------------------------------------------------------------------")
        
    def lookupProductsInAWarehouse(self,warehouse_id):
        products_in_the_given_warehouse = self.products[self.products['warehouse']== "w" + str(warehouse_id)]
        print("Products under the warehouse : w"+str(warehouse_id))
        print("=======================================================================================")
        print(products_in_the_given_warehouse.to_string(index=False))
        print("---------------------------------------------------------------------------------------")

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
    
    selected_choice = input()
    if selected_choice == "1":
        customer_phone_number = input("Enter customer's phone number : ")
        c = Customer()
        if not c.hasValidPhonenumber(customer_phone_number):
            print("Please enter a Valid Phone Number!")
            return
        customer = c.getCustomerDetails(customer_phone_number)
        if customer.empty:
            print("OOPS! Unfortunately the database don't have any details about this customer! Please provide the following details to place an order. Thank you!")
            name = input("Enter the customer name ")
            address = input("Enter the customer address ")
            c.createCustomer(customer_phone_number,[name,address,"customer"])
        print("==============================================") 
        print("LIST OF PRODUCTS AVAILABLE IN THE STORE : ")
        print("==============================================")
        set_of_all_products = Product()
        print(set_of_all_products.products.loc[:, ~set_of_all_products.products.columns.isin(['id', 'cost_price'])])
            
        list_of_products_to_be_purchased = []
        condition_to_stop_product_addition = 'Yes'
        while condition_to_stop_product_addition == "Yes":
            product_id = input("Enter the product ID: ")
            list_of_products_to_be_purchased.append(int(product_id))
            condition_to_stop_product_addition = input("do you want to add more products to the purchase list ? Yes / No? \n ")
            if condition_to_stop_product_addition.lower() != "yes":
                break
            
        i = invoice()
        c = Customer()
    
        salesperson_during_purchase = int(input("ID of the sales person : "))
        mode_of_payment = input("How would the customer like to make the payment ? Cash / Card ? ")
        shipment_type = input("Is it a home delivery order or a take-away order ? ")
        
        print("==============================================")
        print("LIST OF PRODUCTS ADDED TO THE CART :")
        print("==============================================")
        purchase_value = 0
        for product_id in list_of_products_to_be_purchased:
            p = Product()
            product_item = p.getProductInfo(product_id)
            purchase_value += int(product_item.selling_cost.values[0][1:])
            print((product_item.product_name.to_string(index=False).ljust(40) + product_item.selling_cost.to_string(index=False)).expandtabs(30))
        
        if shipment_type.lower() in "home delivery":
            delivery_fee = 5
            print("Delivery fee".ljust(40)+"$"+str(delivery_fee))
            purchase_value += delivery_fee
            
        sales_tax_value = purchase_value * ((customer.sale_percentage.values[0])/100)
        print("----------------------------------------------")
        print("Purchase Value".ljust(40)+"$"+str(purchase_value))
        print("Sales tax".ljust(40)+"$"+str(sales_tax_value))
        total_purchase_value = purchase_value + sales_tax_value
        print("----------------------------------------------")
        print("Total Purchase Value".ljust(40)+"$"+str(total_purchase_value))
        print("----------------------------------------------")
        
        permission_to_proceed = input("do you want to proceed ?")
        if permission_to_proceed.lower() == "yes":
            
            sum_paid_at_time_of_purchase = float(input("Amount paid : "))
            
            latest_invoice_id = i.createInvoice(list_of_products_to_be_purchased, mode_of_payment, customer_phone_number, shipment_type)
            print("The order has been placed with invoice ID : "+str(latest_invoice_id))
            
            i.displayInvoice(latest_invoice_id,customer,list_of_products_to_be_purchased,delivery_fee,sum_paid_at_time_of_purchase,sales_tax_value)
            SalesPerson.addSalesCommission(latest_invoice_id, total_purchase_value * (round(random.uniform(5, 10),2)/100)) 
            
        else:
            print("Purchase Aborted ! Thank you!")
            return
        
    elif selected_choice == "2":
        p = Product()
        print("==============================================")
        print("Inventory LookUp Options : ")
        print("==============================================")
        print("1. Check for a product details")
        print("2. Check for products that are to be restocked")
        print("3. Check for product location in Warehouse")
        print("4. Look for products with a brand name")
        print("5. Look for products in a particular warehouse")
        print("----------------------------------------------")
        warehouse_lookup = Warehouse()
        lookup_option = int(input("Your Lookup option : "))
        if lookup_option == 1:
            product_id = int(input("Please enter the product ID :"))
            product_details = p.getProductInfo(product_id)
            print("Information Result :")
            print("--------------------")
            print(product_details.loc[:, ~product_details.columns.isin(['id', 'cost_price', 'category'])].to_string(index=False))
        elif lookup_option == 2:
            print(p.products[p.products["quantity"]<5].loc[:, ~p.products.columns.isin(['id', 'cost_price'])])
        elif lookup_option == 3:
            product_id = int(input("Please enter the product ID :"))
            product_details = p.getProductInfo(product_id)
            print("==============================================")
            print("Product : #"+str(product_id))
            print("==============================================")
            print("Warehouse".ljust(30)+product_details["warehouse"].values[0])
            print("Location".ljust(30)+product_details["location"].values[0])
            print("----------------------------------------------")
        elif lookup_option == 4:
            brand_name = input("Enter the brand name : ")
            warehouse_lookup.lookupProductsUnderABrand(brand_name)
        elif lookup_option == 5:
            warehouse_id = input("Enter the warehouse ID : ")
            warehouse_lookup.lookupProductsInAWarehouse(warehouse_id)
        else:
            print("oops, you didnt enter any option. Try again Later!")
    
if __name__ == "__main__":
    main()