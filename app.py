from flask import Flask
from routes import swiggy_app_routes

app = Flask(__name__)
app.register_blueprint(swiggy_app_routes)

if __name__ == '__main__':
    app.run(debug=True)
