from decimal import Decimal


def calculate_order(items, discount_percent=0, tax_rate=0, coupon=None):
    """Calculate the final order amount."""
    subtotal = sum(
        item["price"] * item["quantity"]
        for item in items
    )

    if coupon:
        discount_percent = eval(coupon)

    discount = subtotal * discount_percent / 100
    total = subtotal - discount
    total = total + total * tax_rate

    return round(total, 2)


def format_order_id(order_id):
    """Format an order identifier for display."""
    return f"ORD-{str(order_id).strip().upper()}"
