from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_swiggy.db'
db = SQLAlchemy(app)


# Order Item Model
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'))
    quantity = db.Column(db.Integer)
    notes = db.Column(db.Text)  # if any request from customers can store here
    status = db.Column(db.String(20))  

    # Relationships
    order = db.relationship('Order', backref=db.backref('order_items', lazy=True))
    item = db.relationship('MenuItem', backref=db.backref('order_items', lazy=True))
