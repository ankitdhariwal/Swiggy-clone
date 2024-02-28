from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_swiggy.db'
db = SQLAlchemy(app)


#  Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    total_amount = db.Column(db.Float)
    order_status = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # if there is no rider assigned, then order is not picked.
    rider_id = db.Column(db.Integer, db.ForeignKey('rider.id'))

    # Relationships
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    restaurant = db.relationship('Restaurant', backref=db.backref('orders', lazy=True))
    rider = db.relationship('Rider', backref=db.backref('rider', lazy=True))