from app import app
from app.flightBookerDB import db_interface
from app.routes import flights_routes
from flask import request
from app.auth import authUser


@app.route('/bookings/add', methods=['POST'])  # WORKING
def createBooking():
    customerId = authUser(request.headers)
    if not customerId:
        return "unauthorized", 401

    data = request.json
    route = data['route']
    routeClass = data['routeClass']
    route = list(zip(route, routeClass))
    cc = data['cc']
    address = data['address']
    bookingId = db_interface.getLastBookingNumber() + 1

    c = db_interface.conn.cursor()
    c.execute("""INSERT INTO bookings
        (bookingId, customerId, customerCreditCard, customerAddress)
    VALUES (%s, %s, %s, %s);""", (bookingId, customerId, cc, address))

    for flight in route:
        f, cls = flight
        c.execute("INSERT INTO bookingFlights (bookingId, flightId, routeClass) VALUES (%s, %s, %s);", (bookingId, f[0], cls))

    c.close()

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
