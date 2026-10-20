# E-Commerce Order Processing System

This is a small Python project that checks a list of orders and prints a sales report.

## Running it

Open a terminal in this folder and run:


python order_processing_.py


It uses the products and orders already written in the Python file, so there is no setup or extra package to install.

## What the program checks

Orders need a customer name, a valid payment status (`paid` or `pending`), and at least one item. Product IDs must exist and quantities must be positive whole numbers. Orders that fail validation are counted as rejected. Paid orders are also checked against the available stock.

For paid orders, the program works out the subtotal, discount and shipping. Discounts are 5% from $200, 10% from $500, and 15% from $1,000. Shipping is $20 when the discounted subtotal is below $500; otherwise it is free. Pending orders aren't included in sales or stock updates.

The report shows order counts, revenue, discounts, shipping, the top customer, best-selling products and any products with fewer than 10 left.

## Changing the examples

The sample product list and orders are near the top of `order_processing.py`. You can edit them or add your own. For example, an order looks like this:


    "order_id": "ORD004",
    "customer": "Sam",
    "items": [{"product_id": "P005", "quantity": 1}],
    "payment_status": "paid"


The product ID in the order needs to match one in the product list. The program keeps everything in memory, so changes to stock aren't saved after it exits.
