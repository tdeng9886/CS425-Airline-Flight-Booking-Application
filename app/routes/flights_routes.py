from app import app
from app.flightBookerDB import db_interface
from flask import request
from datetime import datetime


@app.route('/flights/airports', methods=['POST'])
def getAirports():
    return db_interface.getAirports()

# Taking two airportIds:
@app.route('/flights/search', methods=['GET', 'POST'])
def routeFlight():
    def routeFlight_rec(cur_airport, arriveTime, arriveAirportId, tokens=5):
        if tokens == 0:
            return False
        routes = []
        subpaths = db_interface.getFlights(cur_airport, arriveTime)
        if subpaths:
            for row in subpaths:
                routes.append([row])
        completed_routes = []
        subroutes = {}
        for route in routes:  # If the end point is where we want to go:
            if route[3] == arriveAirportId:  # If this route ends at the correct place:
                completed_routes.append(route)
            else:  # Otherwise, find it
                subroute = routeFlight_rec(route[3], route[7], arriveAirportId, tokens-1)
                if subroute:
                    subroutes[route] = subroute
        for key in subroutes.keys():
            for subroute in subroutes[key]:
                completed_routes.append(key.extend(subroute))
        return completed_routes

    print(request)
    data = request.json
    print(data)
    departAirportId = data['departAirportId']
    arriveAirportId = data['arriveAirportId']
    departTime = datetime.strptime(data['departTime'], "%Y-%m-%d %H:%M:%S")
    routes = routeFlight_rec(departAirportId, departTime, arriveAirportId)
    return {
        "result": routes
    }
