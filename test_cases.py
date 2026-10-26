# edgecase tests

def run_edge_case_tests():
    import copy
    test_products = copy.deepcopy(products)
    # unknown product
    unknown = {"customer": "Test","items": [{"product_id": "P999", "quantity": 1}],"payment_status": "paid"}
    assert not validate_order(unknown, test_products)[0]

    # zero quantity
    zero = {"customer": "Test","items": [{"product_id": "P002", "quantity": 0}],"payment_status": "paid"}
    assert not validate_order(zero, test_products)[0]

    # negative quantity
    negative = {"customer": "Test","items": [{"product_id": "P002", "quantity": -1}],"payment_status": "paid"}
    assert not validate_order(negative, test_products)[0]

    # quantity greater than stock
    excess = {"customer": "Test","items": [{"product_id": "P001", "quantity": 11}],"payment_status": "paid"}
    assert not validate_order(excess, test_products)[0]

    # empty items
    empty_items = {"customer": "Test","items": [],"payment_status": "paid"}
    assert not validate_order(empty_items, test_products)[0]

    # invalid payment status
    invalid_payment = {"customer": "Test","items": [{"product_id": "P002", "quantity": 1}],"payment_status": "cancelled"}
    assert not validate_order(invalid_payment, test_products)[0]

    # empty products
    assert not validate_order(
        {"customer": "Test",
            "items": [{"product_id": "P001", "quantity": 1}],
            "payment_status": "paid"},{})[0]

    # empty orders
    empty_report = generate_sales_report([], copy.deepcopy(products))
    assert empty_report["total_orders"] == 0
    assert empty_report["revenue"] == 0

    original_stock = products["P001"]["stock"]
    generate_sales_report(orders, products)
    generate_sales_report(orders, products)
    assert products["P001"]["stock"] == original_stock

    # duplicate product exceeding stock.
    duplicate = {"customer": "Test",
        "items": [
            {"product_id": "P001", "quantity": 6},
            {"product_id": "P001", "quantity": 5}
        ],
        "payment_status": "paid"
    }
    assert not validate_order(duplicate, test_products)[0]

    # invalid quantity type
    string_quantity = {"customer": "Test",
        "items": [{"product_id": "P002", "quantity": "2"}],
        "payment_status": "paid"}
    assert not validate_order(string_quantity, test_products)[0]

    # missing items field
    assert not validate_order({"customer": "Test", "payment_status": "paid"},test_products)[0]

    # pending orders must not reduce stock.
    pending_order = {"customer": "Test","items": [{"product_id": "P002", "quantity": 2}],"payment_status": "pending"}
    stock_before = test_products["P002"]["stock"]
    pending_result = process_order(pending_order, test_products)
    assert pending_result["status"] == "pending"
    assert test_products["P002"]["stock"] == stock_before

    # discount and shipping thresholds.
    assert calculate_discount(1000) == 150
    assert calculate_discount(500) == 50
    assert calculate_discount(200) == 10
    assert calculate_discount(199) == 0
    assert calculate_shipping(500) == 0
    assert calculate_shipping(499) == 20
    print("All edge-case tests passed!")


if __name__ == "__main__":
    main()
    run_edge_case_tests()
