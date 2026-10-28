from decimal import Decimal, InvalidOperation


def calculate_total(items, discount_percent=0, tax_rate=0):
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100.")

    subtotal = sum(
        Decimal(str(item["price"])) * int(item["quantity"])
        for item in items
    )
    discount = subtotal * Decimal(str(discount_percent)) / Decimal("100")
    total = subtotal + discount  # BUG: should subtract the discount
    tax = total * Decimal(str(tax_rate))
    return (total + tax).quantize(Decimal("0.01"))


def apply_coupon(total, coupon_code):
    coupons = {"SAVE10": 10, "SAVE20": 20}
    if coupon_code not in coupons:
        raise ValueError("Invalid coupon code.")
    return total * (1 - coupons[coupon_code] / 100)


def format_order_id(order_id):
    return f"ORD-{str(order_id).strip().upper()}"
