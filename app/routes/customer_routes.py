from app import app
import app.auth as auth
from app.flightBookerDB import db_interface
from flask import request
import re


@app.route('/customer/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

@app.route('/customer/create', methods=['POST'])
def createCustomer():
    data = request.json
    name = data['name']
    email = data['email']
    password = data['password']

    # Allow throwing errors (i.e., no email, no password, etc.)
    def isValidEmail(email):
        if len(email) > 7:
        return re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) != None
    
    if (not isValidEmail(email)):
        return {
            'result' : False,
            'message' : 'Invalid email'
        }

    # Checking email
    error = db_interface.checkEmail(email)

    if not error:
        customerId = db_interface.createCustomer(name, email, password)
        return {
            'result': True,
            'customerId': customerId,
            'message': 'Customer has been created.'
        }

    else:
        return {
            'result': False,
            'message': f'The following things failed: {error}.'
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
