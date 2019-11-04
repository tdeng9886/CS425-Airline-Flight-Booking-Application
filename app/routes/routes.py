from app import app
from app.flightBookerDB import db_interface
from flask import request


@app.route('/customer/create', methods=['POST'])
def createCustomer():
    data = request.json
    name = data['name']
    email = data['email']
    password = data['password']

    # Allow throwing errors (i.e., no email, no password, etc.)

    inputValidation = True  # Placeholder.
    error = []

    # Checking email
    inputValidation = inputValidation and db_interface.checkEmail(email)

    if inputValidation:
        customerId = db_interface.createCustomer(name, email, password)

        return {
            'result': True,
            'customerId': customerId,
            'message': 'Customer has been created.'
        }

    else:
        error_string = ", ".join(error)
        return {
            'result': False,
            'message': f'The following things failed: {error_string}.'
        }


@app.route('/customer/address/add', methods=['POST'])
def addCustomerAddress():
    # Getting customer ID from header
    customerId = request.headers.get('customerId')
    # Extracting rest of form data
    data = request.json
    line1 = data['line1']
    line2 = data['line2']
    postalCode = data['postalCode']
    city = data['city']
    state = data['state']
    country = data['country']

    db_interface.addCustomerAddress(customerId, line1, line2, postalCode, city, state, country)

    return {
        'result': True,
        'message': 'Customer address added.'
    }

@app.route('/customer/address/get', methods=['POST'])
def getCustomerAddress():
    customerId = request.headers.get('customerId')
    customerAddresses = db_interface.getCustomerAddresses(customerId)
    if customerAddresses:
        return {
            'result': True,
            'addresses': customerAddresses
        }
    return {
        'result': False
    }

@app.route('/customer/address/delete', methods=['POST'])
def deleteCustomerAddress():
    customerId = request.headers.get('customerId')
    data = request.json
    addressId = data['addressId']
    if deleteCustomerAddress(addressId, customerId):
        return {
            'result': True
        }
    return {
        'result': False
    }


@app.route('bookings/add',methods=['POST'])
def createBooking():
    customerId = request.headers.get('customerId')
    data = request.json
    customerId = data['customerId']
    flightId = data['flightId']

    db_interface.createBooking(customerId, flightId)

    return {
        'result':True,
        'message': 'New bookings has been added.'
    }


@app.route('bookings/get',methods=['POST'])
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
