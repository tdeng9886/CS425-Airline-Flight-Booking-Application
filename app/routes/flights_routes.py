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
    def routeFlight_rec(cur_airport, arriveTime, arriveAirportId, tokens=2):
        if tokens == 0:
            return []
        latestDepart = arriveTime + timedelta(days=1)
        subpaths = [[x] for x in db_interface.getFlights(cur_airport, arriveTime, latestDepart)]
        # print(subpaths)
        # For each possible flight that could be taken first:
        completed_routes = []
        # List of lists (routes)
        for subpath in subpaths:
            if subpath[0][3] == arriveAirportId:
                completed_routes.append(subpath)
            else:
                subsubpaths = routeFlight_rec(subpath[0][3], subpath[0][6], arriveAirportId, tokens-1)
                # Subsubpaths is a list of routes, each leading to the destination.
                for subsubpath in subsubpaths:
                    try:
                        # print(subpath.copy() + subsubpath)
                        if subsubpath != None: # If the last entry in the subsubpath isn't an empty route:
                            completed_routes.append(subpath.copy() + subsubpath) # Then it must lead there
                    except TypeError as E:
                        pass # It's a none value.

        return completed_routes

    data = request.json
    departAirportId = data['departAirportId']
    arriveAirportId = data['arriveAirportId']
    departTime = datetime.strptime(data['departTime'], "%Y-%m-%d %H:%M:%S")
    routes = routeFlight_rec(departAirportId, departTime, arriveAirportId)
    return {
        "result": routes
    }
