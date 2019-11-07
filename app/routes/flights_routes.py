from app import app
from app.flightBookerDB import db_interface
from flask import request

@app.route('/flights/airports', methods=['POST'])
def getAirports():
    return db_interface.getAirports()

# Taking two airportIds:
@app.route('/flights/search', methods=['POST'])
def routeFlight():
    data = request.json

    departAirportId = data['departAirportId']
    departTime = data['departTime']
    end = data['end']
    visited_flights = set()

    def getFlights(departAirportId, departTime):
        return list(db_interface.getFlights(departAirportId, departTime))

    routes = []
    while len(routes) < 10:
        # Begin BFSing until we find a path.
        return None
