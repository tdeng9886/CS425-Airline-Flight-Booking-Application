from app import app
from app.flightBookerDB import db_interface
from flask import request


@app.route('bookings/add', methods=['POST'])
def createBooking():
    customerId = request.headers.get('customerId')
    data = request.json
    customerId = data['customerId']
    flightId = data['flightId']

    db_interface.createBooking(customerId, flightId)

    return {
        'result': True,
        'message': 'New bookings has been added.'
    }


@app.route('bookings/get', methods=['POST'])
def getBooking():
    customerId = request.headers.get('customerId')
    booking = db_interface.getBooking(customerId)
    if booking:
        return {
            'result': True,
            'booking': booking
        }
    return {
        'result': False
    }


@app.route('bookings/delete', methods=['POST'])
def deleteBooking():
    customerId = request.headers.get('customerId')
    data = request.json
    bookingId = data['bookingId']
    if deleteBooking(bookingId, customerId):
        return{
            'result': True
        }
    return {
        'result': False
    }
