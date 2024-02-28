from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_swiggy.db'
db = SQLAlchemy(app)


# Review Model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))

    # Relationships
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    restaurant = db.relationship('Restaurant', backref=db.backref('reviews', lazy=True))

