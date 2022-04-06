import pandas as pd
from csv import writer
from datetime import datetime

class Product:
    # HINT TO TEST THE CODE : 
    # p = Product()
    # p.getProductInfo(1)

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
        
    def createCustomer(self,phone_number, customer_details):
        List = [customer_details[0], phone_number, customer_details[1],"customer"]
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
    # HINT TO TEST THE CODE : 
    # i = invoice()
    # p = Product()
    # c = Customer()
    # ph = PurchaseHistory()

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
        
        newly_created_invoice_id = self.invoice[self.invoice['datetime_of_purchase'] == date_time_value]
        
        p = Product()
        ph = PurchaseHistory()
        for product_id_value in product_id:
            ph.addPurchasedProducts(newly_created_invoice_id,product_id_value,customer_phone_number)
            
            #CALL TO UPDATE PRODUCT QUANTITY
            p.update_product_quantity(product_id_value)
        
        return self.invoice.tail(1).id.values[0]
    

#     def invoiceLookup(self,invoice_params):
#         final_invoice_set = self.invoice[self.invoice['id'] == invoice_id]
#         return final_invoice_set

class PurchaseHistory:
    # ph = PurchaseHistory()
    # ph.addPurchasedProducts(12,123333,datetime.now(),5636738900)
    
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
        # HINTS FOR INPUT : 
        # p = Product()
        # w = Warehouse()
        # w.inventoryLookup(1,4,'LG')
        
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
            
def main():

    print("What would you like to do? Please select one of the following:")
    print("1. Place an order")
    print("2. Inventory Lookup")
    val = input()
    if val == "1":
        customer_phone_number = input("customer_phone_number")
        c = Customer()
        customer = c.getCustomerDetails(customer_phone_number)
        if customer.empty:
            print("OOPS! Unfortunately the database don't have any details about this customer! Please provide the following details to place an order. Thank you!")
            name = input("Enter the customer name")
            address = input("Enter the customer address")
            c.createCustomer(customer_phone_number,[name,address,"customer"])
            
        list_of_products_to_be_purchased = []
        condition_to_stop_product_addition = 'Yes'
        while condition_to_stop_product_addition == "Yes":
            product_id = input("Enter the product ID: ")
            list_of_products_to_be_purchased.append(int(product_id))
            condition_to_stop_product_addition = input("do you want to add more products to the purchase list ? Yes / No?\n")
            if condition_to_stop_product_addition != "Yes":
                break
            
        i = invoice()
        c = Customer()
        print("==============================================")
        print("LIST OF PRODUCTS ADDED TO THE CART :")
        print("==============================================")
        total_purchase_value = 0
        
        for product_id in list_of_products_to_be_purchased:
            p = Product()
            product_item = p.getProductInfo(product_id)
            total_purchase_value += int(product_item.selling_cost.values[0][1:])
            print((product_item.product_name.to_string(index=False).ljust(40) + product_item.selling_cost.to_string(index=False)).expandtabs(30))
        print("----------------------------------------------")
        print("Total Purchase Value".ljust(40)+"$"+str(total_purchase_value))
        print("----------------------------------------------")
        
        mode_of_payment = input("How would the customer like to make the payment ? Cash / Card ? ")
        shipment_type = input("Is it a home delivery order or a take-away order ? ")
        
        
        created_invoice_id = i.createInvoice(list_of_products_to_be_purchased, mode_of_payment, customer_phone_number, shipment_type)
        print("The order has been placed with invoice ID : "+str(created_invoice_id))
        print("==============================================")
        print("INVOICE :")
        print("==============================================")
        
    elif val == "2":
        print("==============================================")
        print("Inventory LookUp Options : ")
        print("==============================================")
        print("1. Check for product availability")
        print("2. Check for products that are to be restocked")
        print("3. Check for product location in Warehouse")
        print("4. Check for product details")
        print("----------------------------------------------")
        
        
    
    
    
if __name__ == "__main__":
    main()