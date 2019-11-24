from app import app
from app.flightBookerDB import db_interface
from flask import request
from datetime import datetime, timedelta
from app.auth import authUser
from dateutil.parser import parse as parse_date


# we could require authentication for these... but that just makes debugging harder

@app.route('/flights/airports', methods=['POST'])  # Working
def getAirports():
    return {
        "airports": db_interface.getAirports()
    }

# Taking two airportIds:
@app.route('/flights/score', methods=['POST'])  # I don't think this should ever be used as an endpoint.
def scoreFlight(route=None, departTime=None):   # In any case, the funtion itself works.
    # Time of Flight
    if not route:
        data = request.json
        route = data['route']
        departTime = datetime.strptime(data['departTime'], "%Y-%m-%d %H:%M:%S")

    flightTime = route[-1][6] - departTime
    # Cost of flight
    ePrice, fPrice = 0, 0
    for flight in route:
        ep, fp = db_interface.getFlightPrice(flight[0])[0]
        ePrice, fPrice = ePrice + float(ep), fPrice + float(fp)
    return (flightTime, ePrice, fPrice) # this would not work as an endpoint as it interprets the tuple as http status values

"""
Inputs:
{
	"departAirportId": "07A",
	"arriveAirportId": "1N7",
	"departTime": "2019-12-29 18:16:52", # Pass as string in this form.
	"tokens": 2, # Suggested value.
	"waitTime": 0.07 # Maximum time beteeen flights, in days.
}

Outputs: """
@app.route('/flights/search', methods=['GET', 'POST'])  # Working
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
    tokens = int(data['tokens'])  # Maximum number of transfers
    waitTime = float(data['waitTime'])  # Maximum number of days between flights

    departTime = parse_date(data['departTime']);

    routes = routeFlight_rec(
        departAirportId, departTime, arriveAirportId, tokens, waitTime
    )

    outputRoutes = {'unsortedRoutes': []}
    for route in routes:
        routeDataTuple = scoreFlight(route, departTime)
        routeData = {
            'routeTime': routeDataTuple[0].total_seconds(),
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

    # 4.3.1 - Skyline Query
    skylineFlights = []
    for testFlight in ecoSortedFlights:
        testPrice = testFlight['routeData']['routeEcoCost']
        testTime = testFlight['routeData']['routeTime']
        skyline = True
        for comparisonFlight in speedSortedFlights:
            comparisonTime = comparisonFlight['routeData']['routeTime']
            comparisonPrice = comparisonFlight['routeData']['routeTime']

            if (testPrice <= comparisonPrice) and (testTime <= comparisonTime):
                if (testPrice < comparisonPrice) or (testTime < comparisonTime):
                    continue
            skyline = False

        if skyline:
            skylineFlights.append(testFlight)



    outputRoutes["speedSortedFlights"] = speedSortedFlights
    outputRoutes["ecoSortedFlights"] = ecoSortedFlights
    outputRoutes["firstSortedFlights"] = firstSortedFlights
    outputRoutes["skylineFlights"] = skylineFlights

    return outputRoutes



@app.route("/flights/<flightId>")
def describeFlight(flightId):
    c = db_interface.conn.cursor()
    c.execute("SELECT airlineId, departAirportId, arriveAirportId, flightNumber, departTime, arriveTime, economySeats, firstClassSeats FROM flights WHERE flightId=%s", (flightId, ))
    r = c.fetchone()
    c.close()

    if not r:
        return 'not found', 404

    return {
        'airline' : r[0],
        'departAirport' : r[1],
        'arriveAirport' : r[2],
        'flightNumber' : r[3],
        'departTime' : r[4],
        'arriveTime' : r[5],
        'economySeats' : r[6],
        'firstClassSeats' : r[7],
    }, 200
