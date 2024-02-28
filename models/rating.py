from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_swiggy.db'
db = SQLAlchemy(app)


# Rating Model
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating_value = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    review_text = db.Column(db.String(200))

    # Relationships
    user = db.relationship('User', backref=db.backref('ratings', lazy=True))
    restaurant = db.relationship('Restaurant', backref=db.backref('ratings', lazy=True))

