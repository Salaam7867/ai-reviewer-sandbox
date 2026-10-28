
import os
from datetime import datetime

from github import Github, GithubException

token = os.getenv("GITHUB_TOKEN")
if not token:
    raise SystemExit("GITHUB_TOKEN is missing.")

repo = Github(token).get_repo("Salaam7867/ai-reviewer-sandbox")
main_branch = repo.default_branch

# Original implementation: deliberately contains bugs.
baseline = '''from decimal import Decimal


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
'''

# The PR attempts to improve validation and monetary precision,
# but deliberately introduces a calculation regression.
challenge = '''from decimal import Decimal, InvalidOperation


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
'''

# Do not overwrite an existing main.py or reuse an old challenge branch.
try:
    repo.get_contents("main.py", ref=main_branch)
    raise SystemExit(
        "main.py already exists on the default branch. "
        "Stopping to avoid overwriting it."
    )
except GithubException as exc:
    if exc.status != 404:
        raise

print(f"Adding baseline main.py to {main_branch}...")
repo.create_file(
    "main.py",
    "test: add order-processing baseline",
    baseline,
    branch=main_branch,
)

# Get the latest default-branch commit after adding the baseline.
main_ref = repo.get_git_ref(f"heads/{main_branch}")
branch_name = "hard-main-py-" + datetime.now().strftime("%Y%m%d-%H%M%S")

repo.create_git_ref(
    ref=f"refs/heads/{branch_name}",
    sha=main_ref.object.sha,
)

# Modify the existing file on the new branch.
file = repo.get_contents("main.py", ref=branch_name)
repo.update_file(
    path="main.py",
    message="test: improve validation but introduce regressions",
    content=challenge,
    sha=file.sha,
    branch=branch_name,
)

pr = repo.create_pull(
    title="test: validate AI reviewer repair and regression detection",
    body=(
        "Deliberate AI PR Reviewer challenge. The patch attempts to improve "
        "discount validation, coupon validation, and monetary precision, "
        "but introduces a discount calculation regression. Do not merge. "
        "Check the diff, repair scope, and runtime behavior."
    ),
    head=branch_name,
    base=main_branch,
)

print("\nChallenge PR created:")
print(pr.html_url)
print(f"Branch: {branch_name}")
print(f"Base: {main_branch}")
