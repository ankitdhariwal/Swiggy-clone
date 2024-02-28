from flask import Flask, request, jsonify
from config import RESTAURANT_TABLE
from utils.files import writeFile, appendFile, readFile
from utils.restaurant_helper import checkDuplicateRestaurant
import os, json
import sys, random

dirname = os.path.dirname
parent_dir = os.path.abspath(os.path.join(dirname(__file__), '..'))
sys.path.append(parent_dir)

file_path = os.path.abspath(os.path.join(parent_dir, "db/{}".format(RESTAURANT_TABLE)))


def registerRestaurant(restaurant_data):
    if not restaurant_data:
        return False
        
    existing_data = readFile(file_path)
    checkDuplicateRestaurant(existing_data, restaurant_data)
    existing_data.append(restaurant_data)
    json_string = json.dumps(existing_data)
    writeFile(file_path, json_string)
    return True


# Dummy data for demonstration
restaurants_dummy_data = [
    {"cuisine_type": ["Italian Delight", "Italian"], "rating" : 4.1, "distance": 3},
    {"cuisine_type": ["Spicy Bites", "Indian"], "rating": 4.0, "distance": 6},
    {"cuisine_type": ["Sushi Haven", "Japanese"], "rating": 4.2, "distance": 8 },
    {"cuisine_type": ["Taco Palace", "Mexican"], "rating":4.5, "distance": 2},
    {"cuisine_type": ["Mexican"], "rating":4.3, "distance": 4},
]


def suggestRestaurantUtil(incoming_data):
    max_distance = incoming_data.get('max_distance')
    cuisine = incoming_data.get('cuisine_type')
    ranked_restaurants = queryRestaurants(cuisine, max_distance)
    if len(ranked_restaurants) == 0:
        return ranked_restaurants

    return ranked_restaurants  # Return top 2 recommendations


def queryRestaurants(cuisine, max_distance=10):
    suggested_restaurant = []
    for restaurant_obj in restaurants_dummy_data:
        if restaurant_obj.get('distance') <= max_distance and cuisine in restaurant_obj.get('cuisine_type'):
            suggested_restaurant.append(restaurant_obj)
    
    if not suggested_restaurant:
        return suggested_restaurant

    sorted_restaurants = sorted(suggested_restaurant, key=lambda k: k['rating'], reverse=True)
    return sorted_restaurants