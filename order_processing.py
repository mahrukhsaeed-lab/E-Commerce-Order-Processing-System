
# E-Commerce Order Processing System

# ====== STARTER DATA ======

products = {
    "P001": {"name": "Laptop", "price": 1200, "category": "Electronics", "stock": 10},
    "P002": {"name": "Mouse", "price": 25, "category": "Accessories", "stock": 50},
    "P003": {"name": "Keyboard", "price": 75, "category": "Accessories", "stock": 20},
    "P004": {"name": "Monitor", "price": 300, "category": "Electronics", "stock": 15}
}

orders = [
    {
        "order_id": "ORD001",
        "customer": "Ali",
        "items": [
            {"product_id": "P001", "quantity": 1},
            {"product_id": "P002", "quantity": 2}
        ],
        "payment_status": "paid"
    },
    {
        "order_id": "ORD002",
        "customer": "Ahmed",
        "items": [
            {"product_id": "P003", "quantity": 2},
            {"product_id": "P004", "quantity": 1}
        ],
        "payment_status": "paid"
    },
    {
        "order_id": "ORD003",
        "customer": "Ali",
        "items": [
            {"product_id": "P002", "quantity": 5}
        ],
        "payment_status": "pending"
    }
]


# ======= HELPER FUNCTION =======

def add_amounts(*amounts):
    return sum(amounts)


# ===== VALIDATION ======

def validate_order(order, products):
    if not isinstance(order, dict):
        return False, "Invalid order format"

    if not isinstance(products, dict) or not products:
        return False, "No products available"

    items = order.get("items")
    customer = order.get("customer")
    payment_status = order.get("payment_status")

    if not isinstance(items, list) or not items:
        return False, "Order has no items"

    if payment_status not in ("paid", "pending"):
        return False, "Invalid payment status"

    if not isinstance(customer, str) or not customer.strip():
        return False, "Invalid customer"

    requested_quantities = {}

    for item in items:
        if not isinstance(item, dict):
            return False, "Invalid item format"

        product_id = item.get("product_id")
        quantity = item.get("quantity")
        if not isinstance(product_id, str):
            return False, "Invalid product ID"

        if product_id not in products:
            return False, "Unknown product ID"

        product = products[product_id]

        if not isinstance(product, dict):
            return False, "Invalid product data"

        price = product.get("price")
        stock = product.get("stock")

        if (isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0):
            return False, "Invalid product price"

        if (isinstance(stock, bool) or not isinstance(stock, int) or stock < 0):
            return False, "Invalid product stock"


        if isinstance(quantity, bool) or not isinstance(quantity, int):
            return False, "Quantity must be a positive integer"

        if quantity <= 0:
            return False, "Quantity must be positive"

        requested_quantities[product_id] = (requested_quantities.get(product_id, 0) + quantity)

    for product_id, quantity in requested_quantities.items():
        if quantity > products[product_id]["stock"]:
            return False, "Insufficient stock"

    return True, "Order is valid"


# ==== SUBTOTAL ===
def calculate_subtotal(order, products):
    line_totals = [products[item["product_id"]]["price"] * item["quantity"] for item in order["items"]]
    
    return round(add_amounts(*line_totals), 2)


# ===== DISCOUNT =====

def calculate_discount(subtotal):
    if subtotal >= 1000:
        discount =subtotal*0.15
    elif subtotal>= 500:
        discount =subtotal*0.10
    elif subtotal >=200:
        discount = subtotal*0.05
    else:
        discount = 0

    return round(discount, 2)


# ====== SHIPPING ======

def calculate_shipping(subtotal,include_shipping=True,free_shipping_threshold=500,shipping_fee=20):
    if not include_shipping:
        return 0
    if subtotal >= free_shipping_threshold:
        return 0
    return round(shipping_fee, 2)


# ===== PROCESS ONE ORDER =======

def process_order(order, products, **options):
    apply_discount = options.get("apply_discount", True)
    include_shipping = options.get("include_shipping", True)
    free_shipping_threshold = options.get("free_shipping_threshold", 500)
    shipping_fee = options.get("shipping_fee", 20)
    if not isinstance(apply_discount, bool):
        return { "status": "rejected","reason": "apply_discount must be True or False"}
    if not isinstance(include_shipping, bool):
        return {"status": "rejected","reason": "include_shipping must be True or False"
        }

    for value in (free_shipping_threshold, shipping_fee):
        if (isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0):
            return {"status": "rejected","reason": "Shipping options must be non-negative numbers" }
    is_valid, message = validate_order(order, products)
    if not is_valid:
        return {"status": "rejected","reason": message}
    subtotal = calculate_subtotal(order, products)

    if order["payment_status"] == "pending":
        return {"status": "pending",
            "subtotal": subtotal,
            "discount": 0,
            "shipping": 0,
            "total": 0,
            "reason": "Payment is pending"}

   
    discount = calculate_discount(subtotal) if apply_discount else 0
    discounted_subtotal = round(subtotal - discount, 2)

    def shipping_fee_for_order():
        if subtotal >= free_shipping_threshold:
            return 0
        return shipping_fee

    shipping = (
        shipping_fee_for_order()
        if include_shipping
        else 0
    )
    total = round(discounted_subtotal + shipping, 2)
    for item in order["items"]:
        product_id = item["product_id"]
        products[product_id]["stock"] -= item["quantity"]

    return {
        "status": "paid",
        "subtotal": subtotal,
        "discount": discount,
        "shipping": shipping,
        "total": total,
        "reason": "Order processed successfully"
    }


# ====== SALES REPORT ======

def generate_sales_report(orders, products, **options):
    if not isinstance(products, dict):
        products = {}
    working_products = {
        product_id: product.copy()
        if isinstance(product, dict)
        else product
        for product_id, product in products.items()
    }

    if not isinstance(orders, list):
        orders = []
        
    paid_orders = []
    pending_orders = []
    rejected_orders = []
    total_revenue = 0
    total_discount = 0
    total_shipping = 0

    spending_by_customer = {}
    sold_quantities = {}

    unique_customers = set()
    unique_categories = {
        product["category"]
        for product in working_products.values()
        if (isinstance(product, dict) and isinstance(product.get("category"), str))}

    for order in orders:
        result = process_order(
            order,
            working_products,
            **options)
        if result["status"] == "rejected":
            order_id = (
                order.get("order_id", "Unknown")
                if isinstance(order, dict)
                else "Unknown"
            )

            rejected_orders.append({
                "order_id": order_id,
                "reason": result["reason"]
            })
            continue
        customer = order["customer"]
        unique_customers.add(customer)
        if result["status"] == "pending":
            pending_orders.append(order)
            continue

        paid_orders.append(order)

       
        total_revenue += result["total"]
        total_discount += result["discount"]
        total_shipping += result["shipping"]

        spending_by_customer[customer] = (
            spending_by_customer.get(customer, 0)
            + result["total"]
        )

        for item in order["items"]:
            product_id = item["product_id"]

            sold_quantities[product_id] = (
                sold_quantities.get(product_id, 0)
                + item["quantity"]
            )

    # round totals to two decimal places.
    total_revenue = round(total_revenue, 2)
    total_discount = round(total_discount, 2)
    total_shipping = round(total_shipping, 2)
    sorted_customers = sorted(
        spending_by_customer.items(),key=lambda customer: customer[1],reverse=True)
    top_customers = []

    if sorted_customers:
        highest_spending = sorted_customers[0][1]

        top_customers = [
            customer
            for customer, spending in sorted_customers
            if spending == highest_spending
        ]
    sorted_products = sorted(sold_quantities.items(),key=lambda product: product[1],reverse=True)
    best_products = []

    if sorted_products:
        highest_quantity = sorted_products[0][1]

        best_products = [working_products[product_id]["name"]
            for product_id, quantity in sorted_products
            if quantity == highest_quantity]

  
    low_stock_limit = options.get("low_stock_limit", 5)

    low_stock_products = {
        product.get("name", product_id): product["stock"]
        for product_id, product in working_products.items()
        if (isinstance(product, dict) and isinstance(product.get("stock"), int) and not isinstance(product.get("stock"), bool) and product["stock"] < low_stock_limit)}

    # return everything 
    return {
        "total_orders": len(orders),
        "paid_orders": len(paid_orders),
        "pending_orders": len(pending_orders),
        "rejected_orders": len(rejected_orders),
        "rejection_details": rejected_orders,
        "revenue": total_revenue,
        "discount": total_discount,
        "shipping": total_shipping,
        "top_customers": top_customers,
        "customer_spending": sorted_customers,
        "best_products": best_products,
        "low_stock": low_stock_products,
        "unique_customers": len(unique_customers),
        "categories": unique_categories
    }


# ===== REPORT OUTPUT ====
def main():
    report = generate_sales_report(orders, products)

    print("========== SALES REPORT ==========\n")
    print(f"Total orders: {report['total_orders']}")
    print(f"Paid orders: {report['paid_orders']}")
    print(f"Pending orders: {report['pending_orders']}")
    print(f"Rejected orders: {report['rejected_orders']}\n")

    print(f"Total revenue: ${report['revenue']:.2f}")
    print(f"Total discount: ${report['discount']:.2f}")
    print(f"Total shipping collected: ${report['shipping']:.2f}\n")

    print(f"Top customer(s): {report['top_customers']}")
    print(f"Best-selling product(s): {report['best_products']}")
    print(f"Low-stock products: {report['low_stock']}")
    print(f"Unique customers: {report['unique_customers']}")
    print(f"Categories: {report['categories']}")

    if report["rejection_details"]:
        print("\nRejected order details:")

        for rejection in report["rejection_details"]:
            print(f"{rejection['order_id']}: "
                f"{rejection['reason']}")


if __name__ == "__main__":
    main()

