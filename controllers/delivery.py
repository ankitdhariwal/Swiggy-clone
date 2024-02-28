
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# This is also keep in redis
# preparation time (in minutes)
restaurant_data = {
    'restaurant_1': 20,
    'restaurant_2': 25,
    'restaurant_3': 30
}

# Restaurant (in kilometers)
# This distance will be calculated in real time from user location to restaurant location using co-ordinates
distance_data = {
    'restaurant_1': 10,
    'restaurant_2': 15,
    'restaurant_3': 20
}
average_speed = 40


def estimateDeliveryTime(restaurant_name):
    # Get preparation time and distance for the restaurant
    preparation_time = restaurant_data.get(restaurant_name)
    distance = distance_data.get(restaurant_name)

    if preparation_time is None or distance is None:
        raise Exception('Restaurant name is invalid')
    
    travel_time = distance/average_speed
    # Add preparation time to travel time
    total_time = preparation_time + travel_time
    return total_time
