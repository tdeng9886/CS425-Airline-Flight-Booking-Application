from flask import Flask
from flask_cors import CORS

app = Flask(__name__, static_url_path='')
CORS(app)

from app.routes import booking_routes, customer_routes, static_routes
