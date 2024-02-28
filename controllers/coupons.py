from flask import Flask, request, jsonify

app = Flask(__name__)

# This coupon_data will kept redis will change dynamic in case of sale, or change acc to time.
# coupon codes and discount values
coupon_data = {
    'MY_SWIGGY10': 10,
    'MY_SWIGGY20': 20,
    'MY_SWIGGY30': 30
}


def calculateTotalOrderDiscountedValue(coupon_code, order_total):
    if coupon_code not in coupon_data:
        raise Exception("Coupon code is invaild")

    discount_percentage = coupon_data.get(coupon_code)
    # Calculate discount amount
    discount_amount = (order_total * discount_percentage) / 100
    # Apply discount to order total
    discounted_total = order_total - discount_amount

    return discounted_total, True
