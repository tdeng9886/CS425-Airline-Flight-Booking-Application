from app import app
from app.flightBookerDB import db_interface
from flask import request
from datetime import datetime, timedelta


@app.route('/flights/airports', methods=['POST'])
def getAirports():
    return db_interface.getAirports()

# Taking two airportIds:
@app.route('/flights/search', methods=['GET', 'POST'])
def routeFlight():
    def routeFlight_rec(cur_airport, arriveTime, arriveAirportId, tokens=3):
        if tokens == 0:
            return False
        routes = []
        latestDepart = arriveTime + timedelta(days=10)
        subpaths = db_interface.getFlights(cur_airport, arriveTime, latestDepart)
        if subpaths:
            for row in subpaths:
                routes.append([row])

        completed_routes = []
        subroutes = {}
        for route in routes:  # If the end point is where we want to go:
            # print(route, "route line 26")
            if route[-1][3] == arriveAirportId:  # If this route ends at the correct place:
                completed_routes.append(route)
            else:  # Otherwise, find it
                print("route", route)
                print("Subrouting: ", route[-1][3], route[-1][7], arriveAirportId, tokens-1)
                subroute = routeFlight_rec(route[-1][3], route[-1][7], arriveAirportId, tokens-1)
                if subroute:
                    subroutes[route] = subroute
        for key in subroutes.keys():
            for subroute in subroutes[key]:
                completed_routes.append(key.extend(subroute))
        return completed_routes


    data = request.json
    departAirportId = data['departAirportId']
    arriveAirportId = data['arriveAirportId']
    departTime = datetime.strptime(data['departTime'], "%Y-%m-%d %H:%M:%S")
    routes = routeFlight_rec(departAirportId, departTime, arriveAirportId)
    return {
        "result": routes
    }
