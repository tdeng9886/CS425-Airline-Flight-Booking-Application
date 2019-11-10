from app import app
from app.flightBookerDB import db_interface
from flask import request


@app.route('/flights/airports', methods=['POST'])
def getAirports():
    return db_interface.getAirports()

# Taking two airportIds:
@app.route('/flights/search', methods=['POST'])
def routeFlight():
    def routeFlight_rec(cur_airport, arriveTime, tokens=5):
        if tokens == 0:
            return False

        routes = []
        completed_routes = []
        for row in db_interface.getFlights(cur_airport, arriveTime):
            routes.append([row])

        subroutes = {}
        for route in routes:  # If the end point is where we want to go:
            if route[3] == end:  # If this route ends at the correct place:
                completed_routes.append(route)
            else:  # Otherwise, find it
                subroute = routeFlight_rec(route[3], route[7], tokens-1))
                if subroute:
                    subroutes[route] = subroute
        for key in subroutes.keys():
            for subroute in subroutes[key]:
                completed_routes.append(key.extend(subroute))

        return completed_routes

    data = request.json
    departAirportId = data['departAirportId']
    departTime = data['departTime']
    end = data['end']

    routes = routeFlight_rec(departAirportId, departTime)
    return route
