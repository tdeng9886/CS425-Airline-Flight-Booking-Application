from app import app
from app.flightBookerDB import db_interface
from app.routes import flights_routes
from flask import request
from app.auth import authUser

''' Input JSON:
{
	 "route": [
        [
          578024,
          "7F",
          "07A",
          "04A",
          50,
          "Sun, 29 Dec 2019 19:45:00 GMT",
          "Mon, 30 Dec 2019 12:15:00 GMT",
          240,
          15
        ],
        [
          306388,
          "3U",
          "04A",
          "1N7",
          47,
          "Mon, 30 Dec 2019 13:45:00 GMT",
          "Mon, 30 Dec 2019 21:45:00 GMT",
          120,
          20
        ]
	 ],
	"routeClass": "economy"
}
'''
@app.route('/bookings/add', methods=['POST'])  # WORKING
def createBooking():
    customerId = authUser(request.headers)
    if not customerId:
        return "unauthorized", 401
    data = request.json
    route = data['route']
    routeClass = data['routeClass']
    bookingId = db_interface.getLastBookingNumber() + 1
    for flight in route:
        db_interface.createBooking(bookingId, customerId, flight[0], routeClass)
    return {
        'message': 'New bookings has been added.'
    }, 200

'''
Only argument is Authentication token in header.
'''
@app.route('/bookings/get', methods=['POST'])  # WORKING
def getBooking():
    customerId = authUser(request.headers)
    if not customerId:
        return "unauthorized", 401
    bookings = db_interface.getBookings(customerId)
    booking_map = {}  # Simplified - form {bookingId: [flight]}
    for booking in bookings:
        if booking[0] in booking_map.keys():
            booking_map[booking[0]]['route'].append(db_interface.getFlightInfo(booking[2]))
        else:
            booking_map[booking[0]] = {
                'route': [db_interface.getFlightInfo(booking[2])],
                'class': booking[3]
            }

    bookingsReturn = {}

    for booking in booking_map.keys():
        route = booking_map[booking]['route']
        deptFlightTime = db_interface.getFlightInfo(route[0][0])[6]
        (flightTime, ePrice, fPrice) = flights_routes.scoreFlight(route, deptFlightTime)
        if booking_map[booking]['class'] == 'economy':
            price = ePrice
        else:
            price = fPrice

        bookingsReturn[booking] = {
            'route': route,
            'routeData': {
                'routeCost': price,
                'flightTime': flightTime.total_seconds(),
            }
        }

    if bookingsReturn:
        return bookingsReturn

    return {
        "message": "No bookings found."
    }, 400

@app.route('/bookings/delete', methods=['POST'])  # WORKING
def deleteBooking():
    customerId = authUser(request.headers)
    if not customerId:
        return "unauthorized", 401
    data = request.json
    bookingId = data['bookingId']
    if db_interface.deleteBooking(bookingId, customerId):
        return {
            "message": "Booking removed."
        }
    return {
        "message": "Failed to remove booking."
    }, 400
