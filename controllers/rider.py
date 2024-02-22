from math import radians, sin, cos, sqrt, atan2
from flask import Flask, request, jsonify
from config import RIDER_TABLE, RIDERS_LOCATION
from utils import writeFile, appendFile, readFile
import os, json
import sys

dirname = os.path.dirname
parent_dir = os.path.abspath(os.path.join(dirname(__file__), '..'))
sys.path.append(parent_dir)

file_path = os.path.abspath(os.path.join(parent_dir, "db/{}".format(RIDER_TABLE)))


def registerRider(rider_data):
    try:
        if not rider_data:
            return False
        existing_data = readFile(file_path)
        existing_data.append(rider_data)
        json_string = json.dumps(existing_data)
        writeFile(file_path, json_string)
        return True
    except Exception as e:
        print(e)
        return False


def findNearestRider(restaurant_location):
    min_distance = float('inf')
    nearest_rider = None
    for rider in RIDERS_LOCATION:
        rider_location = (rider.get('latitude'), rider.get('longitude'))
        distance = calculate_distance(restaurant_location.get('latitude'), restaurant_location.get('longitude'), rider_location[0], rider_location[1])
        if distance < min_distance:
            min_distance = distance
            nearest_rider = rider

    return nearest_rider


def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Earth radius in kilometers
    return distance


rider_locations = {}
def update_location(incoming_data):
    try:
        rider_id = incoming_data.get('rider_id')
        latitude = incoming_data.get('latitude')
        longitude = incoming_data.get('longitude')

        if rider_id is None or latitude is None or longitude is None:
            return jsonify({'error': 'Invalid request incoming_data'}), 400

        rider_locations[rider_id] = {'latitude': latitude, 'longitude': longitude}
        return jsonify({'message': 'Location updated successfully'}), 200
    except Exception as e:
        return 


