from flask import Flask
app = Flask(__name__)
from app.routes import booking_routes, customer_routes, static_routes
