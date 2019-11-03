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
        db_interface.createCustomer(name, email, password)

        return {
            'result': True,
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
