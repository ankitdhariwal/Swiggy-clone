from flask import Flask
from routes import my_swiggy_app_routes

app = Flask(__name__)
app.register_blueprint(my_swiggy_app_routes)

if __name__ == '__main__':
    app.run(debug=True)
