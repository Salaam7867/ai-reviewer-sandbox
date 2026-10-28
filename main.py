from decimal import Decimal


def calculate_total(items, discount_percent=0, tax_rate=0):
    subtotal = sum(
        item["price"] * item["quantity"]
        for item in items
    )
    discount = subtotal * discount_percent / 100
    total = subtotal - discount
    return round(total + total * tax_rate, 2)


def apply_coupon(total, coupon_code):
    coupons = {"SAVE10": 10, "SAVE20": 20}
    return total * (1 - coupons.get(coupon_code, 0) / 100)


def format_order_id(order_id):
    return f"ORD-{str(order_id).strip().upper()}"
