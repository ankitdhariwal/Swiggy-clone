
from flask import Flask, jsonify, request
from flask import Blueprint
from datetime import datetime, timedelta
app = Flask(__name__)
from controllers.rider import (
    updateLocation, registerRider, findNearestRider, getAllOrderbyRider
)
from controllers.user import registerUser
from controllers.restaurant import registerRestaurant, suggestRestaurantUtil
from controllers.order import createNewOrder, getAllOrderByUser
from controllers.delivery import estimateDeliveryTime
from controllers.coupons import calculateTotalOrderDiscountedValue
from controllers.menu import fetchRestaurantMenu


my_swiggy_app_routes = Blueprint('swiggy_routes', __name__)

# API endpoint to health check.
@my_swiggy_app_routes.route('/v1/ping')
def healthCheck():
    return 'Pong', 200


# API endpoint to user register. (1)
@my_swiggy_app_routes.route('/v1/user/register', methods=['POST'])
def userRegisterController():
    try:
        incoming_data = request.json
        username = incoming_data.get('username')
        email = incoming_data.get('email')
        password = incoming_data.get('password')
        phone_number = incoming_data.get('phone_number')

        if not username or not email or not password or not phone_number:
            raise Exception('Missing required fields: username, email, password, or phone_number')

        # if using model
        # if User.query.filter((User.email == email) | (User.phone == phone)).first():
        #     return jsonify({'error-message': 'User with the same email or phone already exists'}), 400

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

    except Exception as e:
        app.logger.error('An error occurred: {}'.format(e))
        return jsonify({'error-message': str(e)}), 400


# API endpoint to rider register. (2)
@my_swiggy_app_routes.route('/v1/rider/register', methods=['POST'])
def riderRegisterController():
    try:
        incoming_data = request.json
        name = incoming_data.get('name')
        email = incoming_data.get('email')
        phone_number = incoming_data.get('phone_number')
        vehicle_type = incoming_data.get('vehicle_type')
        vehicle_registration = incoming_data.get('vehicle_registration')
        
        if not name or not email or not phone_number or not vehicle_type or not vehicle_registration:
            raise Exception('Missing required fields: name, email, phone_number, vehicle_type, or vehicle_registration')

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
    
    except Exception as e:
        app.logger.error('An error occurred: {}'.format(e))
        return jsonify({'error-message': str(e)}), 400


# API endpoint to restaurant register. (3)
@my_swiggy_app_routes.route('/v1/restaurant/register', methods=['POST'])
def restaurantRegisterController():
    try:
        incoming_data = request.json
        name = incoming_data.get('name')
        cuisine = incoming_data.get('cuisine')
        address = incoming_data.get('address')
        phone_number = incoming_data.get('phone_number')
        email = incoming_data.get('email')

        if not name or not cuisine or not address or not phone_number or not email:
            raise Exception('Missing required fields: name, cuisine, address, phone_number, or email')

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
    except Exception as e:
        app.logger.error('An error occurred: {}'.format(e))
        return jsonify({'error-message': str(e)}), 400


# API endpoint to suggest restaurant. (4)
@my_swiggy_app_routes.route('/v1/suggest-restaurant', methods=['POST'])
def suggestRestaurantController():
    try:
        incoming_data = request.json
        suggested_restaurant = suggestRestaurantUtil(incoming_data)
        if len(suggested_restaurant) == 0:
            raise Exception('No restaurants found matching your preferences')

        return jsonify(suggested_restaurant), 200
    except Exception as e:
        app.logger.error('An error occurred: {}'.format(e))
        return jsonify({'error-message': str(e)}), 400


# API to provide a menu for a restaurant. (5)
@my_swiggy_app_routes.route('/v1/restaurants/<restaurant_id>/menu', methods=['GET'])
def getMenuController(restaurant_id):
    # Check if the restaurant ID exists in the menu data
    menu_data = fetchRestaurantMenu(restaurant_id)
    if not menu_data:
        return jsonify({'error-message': 'Restaurant not found'}), 404

    # Retrieve the menu for the specified restaurant ID
    return jsonify({'restaurant_id': restaurant_id, 'menu': menu_data}), 200


# API endpoint to create an order/accpet a order. (6)
@my_swiggy_app_routes.route('/v1/orders/create', methods=['POST'])
def createOrderController():
    try:
        incoming_data = request.json
        user_id = incoming_data.get('user_id')
        restaurant_id = incoming_data.get('restaurant_id')
        total_amount = incoming_data.get('total_amount')
        order_items = incoming_data.get('order_items')  # List of order items

        if not user_id or not restaurant_id or not total_amount or not order_items:
            raise Exception('Missing required fields: user_id, restaurant_id, total_amount, or order_items')

        new_order_data = {
            'user_id': user_id,
            'restaurant_id': restaurant_id,
            'total_amount': total_amount,
            'order_status': 'Pending'
        }

        if createNewOrder(new_order_data, order_items):
            return jsonify({'message': 'Order created successfully', 'order': new_order_data}), 201
        else:
            # We can use re-try mechanism if on 1st time is the order is not place successfully.
            return jsonify({'error-message': 'Unable to create order'}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()
        app.logger.error('An error occurred: {}'.format(e))
        return jsonify({'error-message': str(e)}), 400


# API endpoint to update order status (This will hit from resturant application and rider application)
@my_swiggy_app_routes.route('/v1/orders/<int:order_id>/status', methods=['PUT'])
def updateOrderStatusController(order_id):
    incoming_data = request.json
    new_status = incoming_data.get('order_status')

    if not new_status:
        return jsonify({'error': 'Missing order status'}), 400

    # This will fetch order from order table and update
    # order = Order.query.get(order_id)
    order = True
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    # order.order_status = new_status
    # db.session.commit()

    return jsonify({'message': 'Order status updated successfully', 'order_id': '123'})


# API endpoint to suggest rider (7).
@my_swiggy_app_routes.route('/v1/suggest-rider', methods=['POST'])
def suggestRiderController():
    try:
        incoming_data = request.json
        suggest_rider = findNearestRider(incoming_data)
        if not suggest_rider:
            return jsonify({'error-message': 'No rider found matching your preferences'}), 400 
        
        return suggest_rider
    except Exception as e:
        app.logger.error('An error occurred: {}'.format(e))
        return jsonify({'error-message': str(e)}), 400


# API endpoint to update rider location (8).
@my_swiggy_app_routes.route('/v1/update-rider', methods=['POST'])
def updateRiderController():
    try:
        incoming_data = request.json
        if updateLocation(incoming_data):
            return jsonify({'message': 'Location updated successfully'}), 200
        
        return jsonify({'error-message': 'Location cannot be updated'}), 400
    except Exception as e:
        app.logger.error('An error occurred: {}'.format(e))
        return jsonify({'error-message': str(e)}), 400


# API endpoint to get order history for a user (9)
@my_swiggy_app_routes.route('/v1/orders/history/user/<int:user_id>', methods=['GET'])
def getOrderHistoryUserController(user_id):
    try:
        orders_user_details = getAllOrderByUser(user_id)
        if not orders_user_details:
            return jsonify({'message': 'No orders found for this user'}), 404

        return jsonify({'order_history': orders_user_details}), 200

    except Exception as e:
        app.logger.error('An error occurred: {}'.format(e))
        return jsonify({'error-message': str(e)}), 400


# API endpoint to get order history for a rider (10)
@my_swiggy_app_routes.route('/v1/orders/history/rider/<int:rider_id>', methods=['GET'])
def getOrderHistoryRiderController(rider_id):
    # Fetch orders where rider_id matches and order_status is completed
    orders_rider_details = getAllOrderbyRider(rider_id)
    
    if not orders_rider_details:
        return jsonify({'message': 'No completed orders found for this rider'}), 404

    return jsonify({'order_history': orders_rider_details}), 200


# API endpoint to get Estimate Delivery Time (BONUS-1)
@my_swiggy_app_routes.route('/v1/order/estimate-delivery-time', methods=['GET'])
def getEstimatedDeliveryTimeController():
    try:
        restaurant_name = request.args.get('restaurant_name')
        if not restaurant_name:
            return jsonify({'error-message': 'Restaurant name is required'}), 400

        # Estimate delivery time
        delivery_time = estimateDeliveryTime(restaurant_name)
        # Get current time
        current_time = datetime.now()
        # Calculate estimated delivery time
        estimated_delivery_time = current_time + timedelta(minutes=delivery_time)

        return jsonify({
            'restaurant_name': restaurant_name,
            'estimated_delivery_time': estimated_delivery_time.strftime("%Y-%m-%d %H:%M:%S")
        }), 200
    except Exception as e:
        app.logger.error('An error occurred: {}'.format(e))
        return jsonify({'error-message': str(e)}), 400



# API endpoint to apply coupon for order total get discounted order total (BONUS-2)
@my_swiggy_app_routes.route('/v1/apply-coupon', methods=['POST'])
def applyCouponController():
    try:
        incoming_data = request.json
        coupon_code = incoming_data.get('coupon_code')
        order_total = incoming_data.get('order_total')

        if not coupon_code or not order_total:
            raise Exception('Coupon code and Order total are required')

        discounted_order_total, status = calculateTotalOrderDiscountedValue(coupon_code, order_total)

        if not status or discounted_order_total == -1:
            return jsonify({'error-message': 'Coupon code is invalid'}), 400    

        return jsonify({'discounted_order_total': discounted_order_total}), 200

    except Exception as e:
        app.logger.error('An error occurred: {}'.format(e))
        return jsonify({'error-message': str(e)}), 400
