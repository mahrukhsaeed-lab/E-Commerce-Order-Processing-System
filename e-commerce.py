
# Starter data set
products = {
    "P001": {"name": "Laptop", "price": 1200, "category": "Electronics", "stock": 10},
    "P002": {"name": "Mouse", "price": 25, "category": "Accessories", "stock": 50},
    "P003": {"name": "Keyboard", "price": 75, "category": "Accessories", "stock": 20},
    "P004": {"name": "Monitor", "price": 300, "category": "Electronics", "stock": 15}
}

orders = [
    {
        "order_id": "ORD001", "customer": "Ali",
        "items": [
            {"product_id": "P001", "quantity": 1},
            {"product_id": "P002", "quantity": 2}
        ],
        "payment_status": "paid"
    },
    {
        "order_id": "ORD002", "customer": "Ahmed",
        "items": [
            {"product_id": "P003", "quantity": 2},
            {"product_id": "P004", "quantity": 1}
        ],
        "payment_status": "paid"
    },
    {
        "order_id": "ORD003", "customer": "Ali",
        "items": [{"product_id": "P002", "quantity": 5}],
        "payment_status": "pending"
    }
]



# Validating orders

valid_orders=[]
invalid_orders=[]

def validate_orders(orders, products):
    valid_orders.clear()
    invalid_orders.clear()
    for order in orders:
        valid=True
        
        if not order["items"] or order["payment_status"] not in ["paid", "pending"]:
            valid=False
        for item in order["items"]:
            product_id = item["product_id"]
            quantity = item["quantity"]
            if (product_id not in products or quantity <= 0 or (product_id in products and quantity > products[product_id]["stock"])):
                valid = False
                break
        if valid:
            valid_orders.append(order)
        else:
            invalid_orders.append(order)

    

                
            

# Calculating subtotal
    
orders_subtotal=[]
def calculate_subtotal():
    if not orders:
        print("No orders available!")
        return
    orders_subtotal.clear()
    if valid_orders:
        
        for order in valid_orders:    
            sub_total=0
            name=order['customer']
            for item in order["items"]:
                product_id=item["product_id"]
                quantity=item["quantity"]
                sub_total +=quantity * products[product_id]["price"] 
            orders_subtotal.append({
            "order_id": order["order_id"],
            "customer": name,
            "subtotal": sub_total,
            "quantity": quantity})

            
# Calculate discount                
    
total_discount=0
def calculate_discount():
    global total_discount
    for order in orders_subtotal:
        subtotal=order['subtotal']
        discount=0
        if subtotal >= 1000:
            discount=subtotal*0.15
            
            
        elif subtotal>= 500 and subtotal <1000:
            discount=subtotal*0.1
           
              
        elif subtotal>= 200 and subtotal< 500:
            discount=subtotal*0.05
            
            
        else:
            order['new_subtotal'] = subtotal
            
        total_discount += discount
        order['new_subtotal'] = subtotal - discount        
       
    
# Shipping Calculation

def shipping_calculation():
    global total_shipping_collected
    total_shipping_collected=0
    for order in orders_subtotal:
        subtotal=order['new_subtotal']
        if subtotal >= 500:
            shipping=0
        elif subtotal < 500:
            shipping=20
            subtotal+=20
            total_shipping_collected=shipping
            order['new_subtotal']=subtotal
        order['shipping'] = shipping


     
# Revenue Calculation    

paid_orders=[]
unpaid_orders=[]    
def revenue_calculation():
    global revenue
    revenue=0
    for order in orders:
       
            if order["payment_status"]=="paid":
                paid_orders.append(order)
                
                for subtotal_order in orders_subtotal:
                    if subtotal_order["order_id"]==order["order_id"]:
                        revenue += subtotal_order["new_subtotal"] 
                        break
            else:
                unpaid_orders.append(order)         

# Update Stock        
        
def update_stock():
       
        for order in valid_orders:
            for item in order['items']:
                quantity=item['quantity']
                id=item['product_id']
                stock=products[id]['stock']-quantity
                products[id]['stock']=stock
            
                     
# Checking for the top customer        

top_customer=[]
spending_of_customer={}
max_spending=0
def genrate_customer_report():
    global max_spending
    
    spending_of_customer.clear()
    top_customer.clear()
    max_spending=0
    for order in orders_subtotal:
        name=order['customer']
        subtotal=order['new_subtotal']
        if name in spending_of_customer:
            spending_of_customer[name] += subtotal
        else:
            spending_of_customer[name] = subtotal
   
              
    for customer,subtotal in spending_of_customer.items():
        
        if subtotal>max_spending:
            max_spending=subtotal
            top_customer.append(customer)
        elif subtotal==max_spending:
            top_customer.append(customer)
   
    
# Checking for bst selling product    
    
max_quantity=0 
best_product=[]          
def generate_product_report():
    sold_quanties={}
    global best_product
    global max_quantity
    best_product = []
    max_quantity = 0
    sold_quanties = {}
    
    for order in orders:
        if order['payment_status']=='paid':
            for item in order['items']:
                product_id=item['product_id']
                quantity=item['quantity']
                sold_quanties[product_id] = sold_quanties.get(product_id, 0) + quantity
    for product_id, quantity in sold_quanties.items():            
        if quantity>max_quantity:
            max_quantity=quantity
            best_product = [product_id]
        elif quantity==max_quantity:
            best_product.append(product_id)
                
 
 
# Checking for the products wit low stock         

lowstock_products = {}
def low_stock():
    global lowstock_products
    least_quantity = float('inf')
    lowstock_products.clear()
    low_stock_limit = 5

    for product_id, product in products.items():
        stock =product["stock"]

        if stock < low_stock_limit:
            lowstock_products[product_id] =stock

    if not lowstock_products:
        print("No low-stock products found!")
    else:
        print(lowstock_products)
                        
                        
# Checking for total orders
total_orders=len(orders)
# Rejected orders
rejected_orders=len(invalid_orders)


    
# function calling               
  
validate_orders(orders, products)                
calculate_subtotal()    
calculate_discount()   
shipping_calculation() 
revenue_calculation()
update_stock()
genrate_customer_report()        
generate_product_report()        
low_stock()        
          
          
# Report Output format 
                
print("========== SALES REPORT ==========\n")
print(f"Total orders: {total_orders}")
print(f"Paid orders: {len(paid_orders)}")
print(f"Pending Orders: {len(unpaid_orders)}")
print(f"Rejected orders: {rejected_orders}\n")
print(f"Total revenue: ${revenue}")
print(f"Total discount: ${total_discount}")
print(f"Total shipping: ${total_shipping_collected}\n")
print(f"Top customer: {top_customer}")
print(f"Top selling product: {best_product}\n")
print(f"Low stock products: {lowstock_products}")





    
    
