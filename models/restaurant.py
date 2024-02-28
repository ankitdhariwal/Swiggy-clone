from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_swiggy.db'
db = SQLAlchemy(app)


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    cuisine_type = db.Column(db.String(100))
    contact_number = db.Column(db.String(15))
    rating = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=False)