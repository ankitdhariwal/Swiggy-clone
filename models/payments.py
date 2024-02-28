from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_swiggy.db'
db = SQLAlchemy(app)


# Payment Model
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    amount = db.Column(db.Float)
    payment_status = db.Column(db.String(50))
    payment_method = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime)

    # Relationship
    order = db.relationship('Order', backref=db.backref('payments', lazy=True))
