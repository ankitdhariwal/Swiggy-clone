
from flask import Flask, jsonify, request
from flask import Blueprint
# from controllers.restaurant import 
from controllers.rider import update_location, registerRider, findNearestRider
from controllers.user import registerUser
from controllers.restaurant import registerRestaurant, suggestRestaurantUtil


swiggy_app_routes = Blueprint('swiggy_routes', __name__)


@swiggy_app_routes.route('/v1/ping')
def healthCheck():
    return 'Pong', 200


@swiggy_app_routes.route('/v1/user/register', methods=['POST'])
def userRegisterController():
    incoming_data = request.json
    username = incoming_data.get('username')
    email = incoming_data.get('email')
    password = incoming_data.get('password')
    phone_number = incoming_data.get('phone_number')

    if not username or not email or not password:
        return jsonify({'error-message': 'Missing required fields'}), 400

    user_incoming_data = {
        'user_name': username,
        'email' : email,
        'password': password,
        'phone_number': phone_number
    }

    if registerUser(user_incoming_data):
        return jsonify({'message': 'User: {} has been successfully registered'.format(username)}), 201
    else:
        return jsonify({'error-message': 'Unable to add user'}), 400
    

@swiggy_app_routes.route('/v1/rider/register', methods=['POST'])
def riderRegisterController():
    incoming_data = request.json
    name = incoming_data.get('name')
    email = incoming_data.get('email')
    phone_number = incoming_data.get('phone_number')
    vehicle_type = incoming_data.get('vehicle_type')
    vehicle_registration = incoming_data.get('vehicle_registration')
    
    if not name or not email or not phone_number or not vehicle_type or not vehicle_registration:
        return jsonify({'error-message': 'Missing required fields'}), 400

    rider_incoming_data = {
        "name": name,
        "email" : email,
        "phone_number": phone_number,
        "vehicle_type" : vehicle_type,
        "vehicle_registration": vehicle_registration
    }

    if registerRider(rider_incoming_data):
        return jsonify({'message': 'User {} has been successfully registered'.format(name)}), 201
    else:
        return jsonify({'error-message': 'Unable to add rider'}), 400


@swiggy_app_routes.route('/v1/restaurant/register', methods=['POST'])
def restaurantRegisterController():
    incoming_data = request.json
    name = incoming_data.get('name')
    cuisine = incoming_data.get('cuisine')
    address = incoming_data.get('address')
    phone_number = incoming_data.get('phone_number')
    email = incoming_data.get('email')

    if not name or not cuisine or not address or not phone_number or not email:
        return jsonify({'error': 'Missing required fields'}), 400

    restaurant_incoming_data = {
        "name": name,
        "cuisine": cuisine,
        "address": address,
        "phone_number": phone_number,
        "email": email
    }

    if registerRestaurant(restaurant_incoming_data):
        return jsonify({'message': 'Restaurant Name: {} has been successfully registered'.format(name)}), 201
    else:
        return jsonify({'error-message': 'Unable to add Restaurant'}), 400


@swiggy_app_routes.route('/v1/suggest-restaurant', methods=['POST'])
def suggestRestaurantController():
    incoming_data = request.json
    suggested_restaurant = suggestRestaurantUtil(incoming_data)
    if len(suggested_restaurant) == 0:
        return jsonify({'error-message': 'No restaurants found matching your preferences'}), 400

    return jsonify(suggested_restaurant), 200


@swiggy_app_routes.route('/v1/suggest-rider', methods=['POST'])
def suggestRider():
    incoming_data = request.json
    suggest_rider = findNearestRider(incoming_data)
    if not suggest_rider:
        return jsonify({'error-message': 'No rider found matching your preferences'}), 400 
    
    return suggest_rider


@swiggy_app_routes.route('/v1/update-rider', methods=['POST'])
def updateRider():
    incoming_data = request.json
    if update_location(incoming_data):
        return jsonify({'message': 'Location updated successfully'}), 200
    
    return jsonify({'error-message': 'Location cannot be updated'}), 400


