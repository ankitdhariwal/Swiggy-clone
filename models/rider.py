from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_swiggy.db'
db = SQLAlchemy(app)

# Rider Model
class Rider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(15), unique=True)
    vehicle_number = db.Column(db.String(20))
    vehicle_type = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=False)

