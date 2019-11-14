from app import app
from app.flightBookerDB import db_interface
from flask import request
from datetime import datetime, timedelta


@app.route('/flights/airports', methods=['POST'])
def getAirports():
    return db_interface.getAirports()

# Taking two airportIds:
@app.route('/flights/score', methods=['POST'])
def scoreFlight(route=None, departTime=None):
    # Time of Flight
    if not route:
        data = request.json
        route = data['route']
        departTime = datetime.strptime(data['departTime'], "%Y-%m-%d %H:%M:%S")

    flightTime = route[-1][6] - departTime
    # Cost of flight
    ePrice, fPrice = 0, 0
    for flight in route:
        ep, fp = db_interface.getFlightPrice(flight[0])
        ePrice, fPrice = ePrice + ep, fPrice + fp
    return (flightTime, ePrice, fPrice)


@app.route('/flights/search', methods=['GET', 'POST'])
def routeFlight():
    def routeFlight_rec(cur_airport, arriveTime, arriveAirportId, tokens=2, waitTime=1):
        if tokens == 0:
            return []
        latestDepart = arriveTime + timedelta(days=waitTime)
        subpaths = [[x] for x in db_interface.getFlights(cur_airport, arriveTime, latestDepart)]
        # For each possible flight that could be taken first:
        completed_routes = []
        # List of lists (routes)
        for subpath in subpaths:
            if subpath[0][3] == arriveAirportId:
                completed_routes.append(subpath)
            else:
                subsubpaths = routeFlight_rec(subpath[0][3], subpath[0][6], arriveAirportId, tokens-1, waitTime)
                # Subsubpaths is a list of routes, each leading to the destination.
                for subsubpath in subsubpaths:
                    try:
                        if subsubpath is not None:  # If the last entry in the subsubpath isn't an empty route:
                            completed_routes.append(subpath.copy() + subsubpath) # Then it must lead there
                    except TypeError as E:
                        print(E)
                        pass  # I don't think we should ever hit this.

        return completed_routes

    data = request.json
    departAirportId = data['departAirportId']  # Departing airport
    arriveAirportId = data['arriveAirportId']  # Target airport
    tokens = data['tokens']  # Maximum number of transfers
    waitTime = data['waitTime']  # Maximum number of days between flights

    departTime = datetime.strptime(data['departTime'], "%Y-%m-%d %H:%M:%S")

    routes = routeFlight_rec(
        departAirportId, departTime, arriveAirportId, tokens, waitTime
    )
    '''
    {
        'unsortedRoutes':
            [
                {
                    routeData: {
                        routeTime: timedelta,
                        routeEcoCost: float,
                        routeFirstCost: float
                    },
                    route: [
                        (flight1),
                        (flight2),
                        (...),
                        (flightn)
                    ]
                }
            ],
        'speedSortedRoutes': [
            ...
        ],
        'ecoSortedRoutes': [
            ...
        ],
        'firstSortedRoutes': [
            ...
        ]
    }
    '''

    outputRoutes = {'unsortedRoutes': []}
    for route in routes:
        routeDataTuple = scoreFlight(route, departTime)
        routeData = {
            'routeTime': routeDataTuple[0],
            'routeEcoCost': routeDataTuple[1],
            'routeFirstCost': routeDataTuple[2]
        }
        completeRoute = {
            'routeData': routeData,
            'route': route
        }
        outputRoutes['unsortedRoutes'].append(completeRoute)

    routeSpeed = {}
    routeEcoPrice = {}
    routeFirstPrice = {}

    for route in outputRoutes['unsortedRoutes']:
        routeSpeed[route['routeData']['routeTime']] = route
        routeEcoPrice[route['routeData']['routeEcoCost']] = route
        routeFirstPrice[route['routeData']['routeFirstCost']] = route

    speedSortedFlights = []
    for routeTime in sorted(routeSpeed.keys()):
        speedSortedFlights.append(routeSpeed[routeTime])

    ecoSortedFlights = []
    for price in sorted(routeEcoPrice.keys()):
        ecoSortedFlights.append(routeEcoPrice[price])

    firstSortedFlights = []
    for price in sorted(routeFirstPrice.keys()):
        firstSortedFlights.append(routeFirstPrice[price])

    outputRoutes["speedSortedFlights"] = speedSortedFlights
    outputRoutes["ecoSortedFlights"] = ecoSortedFlights
    outputRoutes["firstSortedFlights"] = firstSortedFlights

    return outputRoutes
