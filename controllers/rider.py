from math import radians, sin, cos, sqrt, atan2
from flask import Flask, request, jsonify
from config import RIDER_TABLE, RIDERS_LOCATION
from utils.files import writeFile, appendFile, readFile
from utils.rider_helper import checkDuplicateRider
import os, json
import sys

dirname = os.path.dirname
parent_dir = os.path.abspath(os.path.join(dirname(__file__), '..'))
sys.path.append(parent_dir)

file_path = os.path.abspath(os.path.join(parent_dir, "db/{}".format(RIDER_TABLE)))


def registerRider(rider_data):
    if not rider_data:
        return False

    existing_data = readFile(file_path)
    checkDuplicateRider(existing_data, rider_data)
    existing_data.append(rider_data)
    json_string = json.dumps(existing_data)
    writeFile(file_path, json_string)
    return True
 

def findNearestRider(restaurant_location):
    min_distance = float('inf')
    nearest_rider = None
    # RIDERS_LOCATION is updated in redis for real time RIDERS_LOCATION is coming from redis
    # restaurant_location will coming from DB, has it already fixed, now taking it coming from front end.
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


def updateLocation(incoming_data):
    rider_id = incoming_data.get('rider_id')
    latitude = incoming_data.get('latitude')
    longitude = incoming_data.get('longitude')

    if rider_id is None or latitude is None or longitude is None:
        raise Exception('Invalid request incoming_data')

    for index in range(len(RIDERS_LOCATION)):
        if RIDERS_LOCATION[index].get('id') == rider_id:
            RIDERS_LOCATION[index]['latitude'] = latitude
            RIDERS_LOCATION[index]['longitude'] = longitude
            return True

    raise Exception('rider_id is invalid')


def getAllOrderbyRider(rider_id=None):
    existing_data = readFile(file_path)
    if len(existing_data) == 0:
        raise Exception("No orders found for this rider")

    all_orders_list = []
    for index in range(len(existing_data)):
        if existing_data[index].get('rider_id') == rider_id:
            all_orders_list.append(existing_data[index])

    return all_orders_list
