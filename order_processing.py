from decimal import Decimal


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



#Validating orders
valid_orders=[]
invalid_orders=[]

def validate_orders(orders, products):
    valid_orders.clear()
    invalid_orders.clear()
    paid_quantities = {}
    for order in orders:
        valid = isinstance(order, dict)
        if valid:
            valid = (
                isinstance(order.get("customer"), str)
                and bool(order["customer"].strip())
                and order.get("payment_status") in ("paid", "pending")
                and isinstance(order.get("items"), list)
                and bool(order["items"])
            )

        requested_quantities = {}
        if valid:
            for item in order["items"]:
                if not isinstance(item, dict):
                    valid = False
                    break
                product_id = item.get("product_id")
                quantity = item.get("quantity")
                if (not isinstance(product_id, str) or product_id not in products or not isinstance(quantity, int) or isinstance(quantity, bool)
                    or quantity <= 0):
                    valid = False
                    break
                requested_quantities[product_id] = (requested_quantities.get(product_id, 0) + quantity)
        if valid:
            for product_id, quantity in requested_quantities.items():
                available_stock = products[product_id]["stock"]
                if order["payment_status"] == "paid":
                    available_stock -= paid_quantities.get(product_id, 0)
                if quantity > available_stock:
                    valid = False
                    break

        if valid:
            valid_orders.append(order)
            if order["payment_status"] == "paid":
                for product_id, quantity in requested_quantities.items():
                    paid_quantities[product_id] = (paid_quantities.get(product_id, 0) + quantity)
        else:
            invalid_orders.append(order)



# calculating subtotal
def calculate_subtotal(products):
    for order in valid_orders:
        order["subtotal"] = sum((Decimal(products[item["product_id"]]["price"])* item["quantity"] for item in order["items"]))
        


# calculating discount
def calculate_discount():
    global total_discount
    total_discount = Decimal("0")
    for order in valid_orders:
        subtotal = order["subtotal"]
        discount = Decimal("0")
        if order["payment_status"] == "paid":
            if subtotal >= 1000:
                discount = subtotal * Decimal("0.15")
            elif subtotal >= 500:
                discount = subtotal * Decimal("0.10")
            elif subtotal >= 200:
                discount = subtotal * Decimal("0.05")
            total_discount += discount
        order["discount"] = discount
        order["subtotal"] = subtotal - discount


# Calculating shipping for the orders
def shipping_calculation():
    global total_shipping_collected
    total_shipping_collected=Decimal("0")
    for order in valid_orders:
        shipping = Decimal("0")
        if order["payment_status"]== "paid" and order["subtotal"] < 500:
            shipping =20
            total_shipping_collected +=shipping
        order["shipping"]=shipping
        order["total"]=order["subtotal"] + shipping



# Calculating revenue of company
paid_orders = []
pending_orders = []
def revenue_calculation(orders, products):
    global revenue
    revenue = Decimal("0")
    paid_orders.clear()
    pending_orders.clear()
    for order in valid_orders:
        if order["payment_status"]=="paid":
            paid_orders.append(order)
            revenue+=order["subtotal"]
        else:
            pending_orders.append(order)


# updating stock after evaulating paid orders
stock_updated_orders=set()
def update_stock():
    for order in valid_orders:
        order_identity=id(order)
        if (order["payment_status"]=="paid"and order_identity not in stock_updated_orders):
            for item in order["items"]:
                product_id =item["product_id"]
                products[product_id]["stock"] -=item["quantity"]
            stock_updated_orders.add(order_identity)
            
            

# Finding top customer            
top_customer=[]
spending_of_customer={}
max_spending=0
def generate_customer_report():
    global max_spending
    max_spending=0
    spending_of_customer.clear()
    top_customer.clear()

    for order in valid_orders:
        name=order["customer"]
        subtotal=order["subtotal"]
        if order["payment_status"]=="paid":
            if name in spending_of_customer:
                spending_of_customer[name]+=subtotal
            else:
                spending_of_customer[name]=subtotal

    for customer, subtotal in spending_of_customer.items():
        if subtotal > max_spending:
            max_spending=subtotal
            top_customer.clear()
            top_customer.append(customer)
        elif subtotal==max_spending:
            top_customer.append(customer)



# Finding best selling product
def generate_product_report():
    sold_quantities={}
    global best_product
    global max_quantity
    best_product=[]
    max_quantity=0
   
    
    for order in valid_orders:
        if order["payment_status"]=="paid":
            for item in order["items"]:
                product_id=item["product_id"]
                quantity=item["quantity"]
                sold_quantities[product_id] = sold_quantities.get(product_id, 0) + quantity
    for product_id, quantity in sold_quantities.items():
        product_name=products[product_id]["name"]
        if quantity > max_quantity:
            max_quantity=quantity
            best_product=[product_name]
        elif quantity==max_quantity:
            best_product.append(product_name)


# checking for lowstock products
lowstock_products={}
def low_stock():
    global lowstock_products
    lowstock_products.clear()
    low_stock_limit = 10

    for product in products.values():
        stock=product["stock"]
        name=product["name"]
        if stock<low_stock_limit:
            lowstock_products[name]=stock
    return lowstock_products


 # main 
def main():
    validate_orders(orders, products)
    calculate_subtotal(products)
    calculate_discount()
    shipping_calculation()
    revenue_calculation(orders, products)
    update_stock()
    generate_customer_report()
    generate_product_report()
    low_stock()

    print("========== SALES REPORT ==========\n")
    print(f"Total orders: {len(orders)}")
    print(f"Paid orders: {len(paid_orders)}")
    print(f"Pending Orders: {len(pending_orders)}")
    print(f"Rejected orders: {len(invalid_orders)}\n")
    print(f"Total revenue: ${revenue}")
    print(f"Total discount: ${total_discount}")
    print(f"Total shipping: ${total_shipping_collected}\n")
    print(f"Top customer: {(top_customer) or 'None'}")
    print(f"Top selling product: {(best_product) or 'None'}\n")
    print(f"Low stock products: {lowstock_products}\n")
    print("==================================")

if __name__ == "__main__":
    main()
