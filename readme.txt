Main face will be 3 applications
1) Customer's Application
2) Rider's Application
3) Admin/ Restaurant Application

=================================
DATABASE DESIGN 
=================================

Users Table:
user_id (Primary Key)
username
email
password_hash
phone_number
address


Restaurants Table:
restaurant_id (Primary Key)
name
address
contact_number
cuisine_type (json)
rating

Rider Table:
rider_id
name 
email
password_hash
phone_number
address
vehicle_type
vechile_no
rating
Availability

Ratings Table:
RatingID (Primary Key)
RiderID (Foreign Key)
CustomerID (Foreign Key) (JSON)
Rating
Review Text


Menu Items Table:      
item_id (Primary Key)
restaurant_id (Foreign Key)
name
description
price


Orders Table:
order_id (Primary Key)
user_id (Foreign Key)
restaurant_id (Foreign Key)
order_time
delivery_address
total_amount
status (pending, preparing, on the way, delivered)


Order Items Table:
order_item_id (Primary Key)
order_id (Foreign Key) (Orders Table)
item_id (Foreign Key) (Menu Table)
quantity
item_price


Payment Table:
payment_id (Primary Key)
order_id (Foreign Key)
payment_time
payment_method
amount


Reviews Table: (This table will later update the restaurant table)
review_id (Primary Key)
user_id (Foreign Key)
restaurant_id (Foreign Key)
rating
comment
review_time


Other tables
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


2) User Registration:

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

3) Rider Registration:
Endpoint: /v1/rider/register
will same as of 2


4) Restaurant Registration:
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


9) Menu Retrieval: (5)
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


10) Accept Order: (6)
Endpoint: /v1/orders
Methods: POST
Request Body:
{
  "restaurant_id": 1,
  "items": [
      {
          "item_id": 1,
          "quantity": 1
      },
      {
          "item_id": 2,
          "quantity": 1
      }
  ],
  "delivery_address": "123, New Delhi"
}

Response:
{
    "message": "Order placed successfully"
}


11) Order Status: 
Endpoint: /v1/orders/{order_id}/status
Methods: GET
{
    "status": "Delivered"
}

There can two API's for: (GET)
12)order history for the customer , on basics user_id 
13) order completed by the rider , by rider_id


Other API's can be
14) Review for rider, customer, restaurant
15) Analytics
16) Coupons API


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


