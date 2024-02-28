Main face will be 3 applications
1) Customer's Application (APP)
2) Rider's Application (APP)
3) Admin/ Restaurant Application (APP)


Coupons System - only single API for apply coupon made, seperate two tables can be there:
1) Coupons
2) Deals

For type and that is user name is string , phone number is alpha-numeric , 
These checks are mainly handled on front end, I am expecting that data types will be correct
from input.
we can use object serialization, like Schema, fields that will handle the tpe check while
updating the tables.

ORM USED - MODELS and SQLAlchemy (flask ORM)
- ALL TABLES HAVE BEEN MADE WITHIN MODELS
- BUT FOR LOCAL FUNCTIONALITIES DATA IS STORED IN db/{db}.json files


- Updating rider location
1) In real time , Scheduled Job will run to latitude, longitude of a rider , will place that
in redis then, restaurant co-ordinates value will fixed , it will come from either DB or front end.


- Some Things for fast in developemnt , used some assumptions, that mention in each API comment wise.


=================================
DATABASE DESIGN
=================================

=====> Users Table <=====
user_id (Primary Key)
username
email
password_hash
phone_number
address


=====> Restaurants Table <=====
restaurant_id (Primary Key)
name
address
contact_number
cuisine_type (json)/ (string)
rating
is_active


=====> Rider Table <=====
rider_id (Primary Key)
name 
email
password_hash
phone
address
vehicle_type
vechile_no
rating
is_active


=====> Ratings Table <=====
id (Primary Key)
rating_value
user_id (Foreign Key) (users)
restaurant_id (Foreign Key) (restaurant)
review_text


=====> Menu Items Table <=====     
item_id (Primary Key)
restaurant_id (Foreign Key) (restaurant)
name
description
price


=====> Orders Table <=====
order_id (Primary Key)
user_id (Foreign Key)
restaurant_id (Foreign Key)
order_time
delivery_address
total_amount
rider_id (Foreign Key) (Rider Table)
status (pending, preparing, on the way, delivered)


=====> Order Items Table <=====
order_item_id (Primary Key)
order_id (Foreign Key) (Orders Table)
item_id (Foreign Key) (Menu Table)
quantity
notes 
status


=====> Payment Table <=====
payment_id (Primary Key)
order_id (Foreign Key) (order table)
amount
payment_status
payment_time
payment_method
amount


=====> Reviews Table: (This table will later update the restaurant table) <=====
review_id (Primary Key)
user_id (Foreign Key)
restaurant_id (Foreign Key)
rating
comment
review_time


=====> Other tables that can be made - on  <=====
1) Coupons
2) Deals



=================================
API DESIGN 
=================================


1) User Authentication: 

Endpoint: /v1/auth
Methods: POST

Request Body:

{
    "username": "user@example.com",
    "password": "password123"
}

Response:
{
    "token": "JWT_TOKEN"
}


2) User Registration: (1)

Endpoint: /v1/user/register
Methods: POST
Request Body:
{
    "username": "user@example.com",
    "password": "password123",
    "phone_number": "1234567890",
    "address": "123, NEW DELHI"
}
Response:
{
    "message": "User registered successfully"
}


3) Rider Registration: (2)
Endpoint: /v1/rider/register
Request Body:
{
    "name": "John Doe",
    "email": "john_1@example.com",
    "phone_number": "1234567891",
    "vehicle_type": "Motorcycle",
    "vehicle_registration": "ABC123"
}
Response:
{
    "message": "User John Doe has been successfully registered"
}



4) Restaurant Registration: (3)
Endpoint: /v1/restaurant/register
Methods: POST
Request Body:
{
    "name": "Restaurant-123",
    "cuisine": "Italian",
    "address": "123 Main St, City, Country",
    "phone_number": "1234567890",
    "email": "restaurant@example.com"
}
Response:
{
    "message": "Restaurant registered successfully"
}



5) Suggest a restaurant to a user basics (4)
Endpoint: /v1/suggest-restaurant
Methods: POST
Request Body:
{
    'meal_time': 'dinner',
    'max_distance': 5,
    "cuisine_type": ["Italian"]
}

Response:
[
  {
    "id": 1,
    "name": "Restaurant A",
    "address": "123, NEW DELHI",
    "cuisine_type": ["Italian"],
    "rating": 4.5
  },
  {
    "id": 2,
    "name": "Restaurant B",
    "address": "456, Mumbai",
    "cuisine_type": ["Mexican"],
    "rating": 4.2
  }
]

6) Restaurant Listings:
Endpoint: /v1/restaurants-list
Methods: GET

Response:
[
  {
    "id": 1,
    "name": "Restaurant A",
    "address": "123, NEW DELHI",
    "cuisine_type": ["Italian"],
    "rating": 4.5
  },
  {
    "id": 2,
    "name": "Restaurant B",
    "address": "456, Mumbai",
    "cuisine_type": ["Mexican"],
    "rating": 4.2
  }
]


7) Find a rider nearest to the restaurant to pick up the order  

Endpoint: /v1/suggest-rider
Methods: POST
Request Body:
{'restaurant_location': ['40.7128', '-74.0060']}

Response:
{'id': 2, 'latitude': 40.7127, 'longitude': -74.0061}


8) update location of rider 

Endpoint: /v1/update-rider
Methods: POST
Request Body:
{
    "rider_id": 1,
    "latitude": 40.7128,
    "longitude": -74.0060
}

Response:
{"message": "Rider location successfully updated"}


9) Menu Retrieval: (5).
Endpoint: /v1/restaurants/{restaurant_id}/menu
Methods: GET
Response:
[
  {
    "id": 1,
    "name": "Pizza",
    "description": "Cheese, tomato sauce, toppings",
    "price": 400
  },
  {
    "id": 2,
    "name": "Pasta",
    "description": "Spaghetti, marinara sauce, parmesan cheese",
    "price": 250
  }
]


10) Accept Order: (6).
Endpoint: /v1/orders/create
Methods: POST
Request Body:
{
    "user_id": "123456",
    "restaurant_id": "789012",
    "total_amount": 250.50,
    "order_items": [
        {"item_id": "item_1", "name": "Pizza", "quantity": 2, "price": 100.00},
        {"item_id": "item_2", "name": "Coke", "quantity": 1, "price": 50.50},
        {"item_id": "item_3", "name": "Garlic Bread", "quantity": 1, "price": 50.00}
    ]
}

Response:
{
    "message": "Order created successfully",
    "order": {
        "order_status": "Pending",
        "restaurant_id": "789012",
        "total_amount": 250.5,
        "user_id": "123456"
    }
}


11) Order Status: 
Endpoint: /v1/orders/{order_id}/status
Methods: GET
Response:
{
    "status": "Delivered"
}


12) Estimate Delivery Time
EndPoint:  v1/order/estimate-delivery-time?restaurant_name=restaurant_1
Methods: GET
Response:
{
    "estimated_delivery_time": "2024-02-28 09:35:37",
    "restaurant_name": "restaurant_1"
}


13) Apply coupon
EndPoint: v1/apply-coupon
Methods: POST
Request Body:
{
    "order_total": 250,
    "coupon_code": "MY_SWIGGY20"
}
Response:
{
    "discounted_order_total": 200.0
}



===================================
BONUS REQUIREMENTS
===================================

Approach to estimate the delivery time:

Calculate the Preparation Time: Retrieve the average preparation time for orders from each restaurant. This can be based on historical data or predefined estimates.
Calculate the Distance: Use a mapping service (e.g., Google Maps API) to calculate the distance between the restaurant and the delivery location.
Estimate Travel Time: Use the estimated distance and current traffic conditions (if available) to estimate the travel time from the restaurant to the delivery location.
Calculate Total Time: Add the preparation time and travel time to get the total estimated delivery time.
Consider Other Factors: Factor in additional time for unexpected delays, peak hours, or busy periods.


=================================
Different Componet / Services
=================================


1) User Service:
- Responsible for managing user accounts, authentication, and authorization.
- Handles user registration, login, profile management, and password reset functionalities.


2) Restaurant Service:
- Manages restaurant related operations such as restaurant listings , reviews.
- Handles CRUD (Create, Read, Update, Delete) operations for restaurants and their menus.
- Provides functionalities for restaurant owners to update their information and manage orders.


3) Order Service:
- Handles order management, including order placement, order tracking, and order history.
- Manages the lifecycle of orders from placement to delivery.


4) Delivery Service:
- Manages delivery operations, including assigning delivery executives,
tracking delivery status, and optimizing delivery routes.
- Handles communication between delivery boy and customers for order delivery updates.
Optimizes delivery processes for faster and more efficient order fulfillment.


5) Payment Service:
- Integrates with payment gateways to handle payment processing securely.
- Manages payment transactions, refunds, and payment status updates.
- Practice security standards.


6) Notification Service:
- Sends out real-time notifications to users regarding order updates, promotions, and other important information.


7) Analytics Service: (BONUS)
- Collects and analyzes data related to user behavior, order trends, and performance metrics.
- Provides insights to improve user experience, optimize business operations, and drive strategic decision-making.



=================================
APPLICATION FLOW
=================================

Microservices-based architecture here.

1)user registration, order management, and payment management use transactional databases.
2) The system will use a relational database for rest services.

3) Information about restaurants, menus, prices, and offers will be stored in ElasticSearch, a JSON document storage that provides fast and scalable search options.
4) The ordering process includes choosing Restaurant > selecting dishes > calculating prices > processing payments through different payment gateways and options. 

5) Once an order is successfully placed, the information is sent to a central message queue,
such as RabbitMQ/Redis Queue.
6) Order processing unit reads the order information, notifies the selected restaurant,
and searches for available delivery partners nearby.
7) Customers receive push notifications about their orders and can track their order status and the live location of the delivery person through the order processing and tracking service.
8) The delivery person then picks up the order and delivers it to the customer, with real-time notifications of the estimated arrival time.



The delivery prediction and assignment service continuously update the pool of 
available delivery persons for different areas to ensure efficient and timely delivery.


=================================
CUSTOMER FLOW
=================================

1) When a customer opens the app, the first call is made to the Inventory/Menu system to determine the following:

2) Nearby serviceable restaurants to customer locations. This is done by comparing the customer's location to the location of the restaurants.
3) The restaurants that can deliver food within a specific time frame, such as 45 minutes.
4) The expected delivery time for the customer's food order from a potential restaurant. 
5) This is based on factors such as the distance to the restaurant, the 
restaurant's preparation time, and the availability of delivery partners in the area.
6) This helps the customer quickly find nearby serviceable restaurants and get an 
idea of expected delivery times so they can make an informed decision about which 
restaurant to order from.


================================================================
HANDLE Scalability in MY_SWIGGY APP
================================================================

1) Use a microservices architecture where different components of your application 
can scale independently. This allows you to scale specific parts of your 
system based on demand. Horizontal Scaling

2) sharding techniques to distribute the database workload across multiple nodes.

3) Use caching mechanisms like Redis or Memcached to cache frequently accessed 
data and reduce the load on your database. 

4) Offload long-running or resource-intensive tasks to background jobs or message 
queues. Use asynchronous processing for tasks like order processing, notifications, 
and data processing to free up resources and improve the responsiveness of your 
application.

5) Monitoring, Alerting -> health check and if any goes down .  Set up auto-scaling mechanisms  in response to changes in traffic or workload.

6) Performance Optimization and Capacity Planning ie (growth projections and historical data) Plan ahead for scaling your infrastructure and resources to meet future demand.
