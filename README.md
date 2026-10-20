# E-Commerce-Order-Processing-System

A small Python program that validates sample orders and prints a sales report. The product catalog and orders are stored directly in `order_processing.py`; the program does not use a database or external packages.

## Requirements

- Python 3.8 or newer

## Run

Open a terminal in the project folder and run:

```powershell
python order_processing.py
```

## What it does

The program processes the sample data in this order:

1. Validates each order. An order must have a non-empty customer name, a `paid` or `pending` payment status, at least one item, known product IDs, positive integer quantities, and enough available stock for paid orders. Invalid orders are counted as rejected.
2. Calculates each valid order's item subtotal.
3. Applies a discount to paid orders:
   - 15% for subtotals of $1,000 or more
   - 10% for subtotals of $500 or more
   - 5% for subtotals of $200 or more
4. Adds $20 shipping to paid orders with a post-discount subtotal under $500. Shipping is free for other paid orders. Pending orders are not charged.
5. Calculates the report totals and customer/product summaries from valid orders. Only paid orders count toward revenue, discounts, customer spending, products sold, and stock reduction.
6. Lists products with fewer than 10 units remaining.

The printed report includes total, paid, pending, and rejected order counts; revenue, discounts, and shipping collected; the top customer; best-selling product(s); and low-stock products.

## Change the sample data

Edit `products` and `orders` near the top of `order_processing.py`.

Each product is keyed by a product ID and has a name, price, category, and stock count:

```python
"P005": {
    "name": "Headphones",
    "price": 80,
    "category": "Accessories",
    "stock": 12,
}
```

An order has a customer, payment status, and a list of product IDs and quantities:

```python
{
    "order_id": "ORD004",
    "customer": "Sam",
    "items": [{"product_id": "P005", "quantity": 1}],
    "payment_status": "paid",
}
```

## Notes

- Prices and calculated money use Python's `Decimal` type.
- Data is kept in memory. Changes made while the program runs are not saved when it exits.
