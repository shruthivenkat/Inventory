import pandas as pd
from csv import writer


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
    def createCustomer(phone_number, customer_details):
        List = [customer_details[0], phone_number, customer_details[1]]
        with open('customer_ASE.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(List)
            f_object.close()
        
    def getCustomerDetails(phone_number):
        customer = pd.read_csv (r'customer_ASE.csv')
        customer.reset_index(inplace=True)
        customer = customer.rename(columns = {'index':'id'})
        val = customer[customer['phone_number']==phone_number] 
        return val 

class invoice(Product):
    # HINT TO TEST THE CODE : 
    # i = invoice()
    # p = Product()
    # i.createInvoice(1,'cash',333224,'shruthi','123 Ave')

    def __init__(self):
        self.invoice = pd.read_csv (r'invoice_ASE.csv')
        self.invoice.reset_index(inplace=True)
        self.invoice = self.invoice.rename(columns = {'index':'id'})
        
    def createInvoice(self,product_id, mode_of_payment, phone_number, *name, **address):
        #HINT FOR CALLING THIS FUNCTION : invoice.createInvoice(1,'cash',12234,'shruthi','123 Ave')
        
        customer = Customer.getCustomerDetails(phone_number)
        if customer.empty:
            Customer.createCustomer(phone_number, name)
            customer = Customer.getCustomerDetails(phone_number)
            
        List = [product_id,mode_of_payment,customer.id.values[0]]

        with open('invoice_ASE.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(List)
            f_object.close()
            
        #CALL TO UPDATE PRODUCT QUANTITY
        p.update_product_quantity(product_id)
        
    def invoiceLookup(self,invoice_id):
        final_invoice_set = self.invoice[self.invoice['id'] == invoice_id]
        return final_invoice_set

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



class admin()
	passwordCheck()
