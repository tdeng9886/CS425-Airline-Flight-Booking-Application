import psycopg2

conn = psycopg2.connect(dbname='flights425', user='postgres', password='space')
conn.autocommit = True
from app.auth import hashPassword

# don't forget to conn.close() and cursor.close()
def newConnection():
    return psycopg2.connect(dbname='flights425', user='postgres', password='space')


def checkEmail(email):  # Returns True if email not in DB, False if it is.
    c = conn.cursor()
    c.execute("SELECT email FROM customers WHERE email LIKE %s;", (email,))
    if c.fetchone():
        c.close()
        return False
    c.close()
    return True

def addCustomerAddress(addressId, customerId, line1, line2, postalCode, city, state, country):
    c = conn.cursor()
    c.execute("INSERT INTO customerAddresses VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (
        addressId,
        customerId,
        line1,
        line2,
        postalCode,
        city,
        state,
        country)
    )
    c.close()
    return True

def getLastAddressNumber():
    c = conn.cursor()
    c.execute("SELECT addressId FROM customerAddresses ORDER BY customerAddresses DESC LIMIT 1")

    if c.rowcount == 0:
        return 0
    else:
        ret = c.fetchone()[0]
        c.close()
        return ret



def getCustomerAddresses(customerId):
    #print("cid:", customerId, flush=True);
    c = conn.cursor()
    c.execute("SELECT addressId, line1, line2, postalCode, city, state, country FROM customerAddresses WHERE customerId = %s", (customerId,))
    ret = c.fetchall()

    ret = list(map(lambda t: {
            "addressId" : t[0],
            "line1": t[1],
            "line2": t[2],
            "postalCode": t[3],
            "city": t[4],
            "state" : t[5],
            "country" : t[6],
            }, ret))
    print(ret, flush=True)
    c.close()
    return ret



def deleteCustomerAddress(addressId, customerId):
    c = conn.cursor()
    c.execute("DELETE FROM customerAddresses WHERE addressId = %s AND customerId = %s", (addressId, customerId))
    rows_deleted = c.rowcount
    return bool(rows_deleted)


def createBooking(bookingId, customerId, flightId, routeClass):
    c = conn.cursor()
    c.execute("INSERT INTO bookings VALUES (%s,%s,%s,%s)", (
            bookingId,
            customerId,
            flightId,
            routeClass)
    )
    c.close()
    return True


def getBookings(customerId):
    c = conn.cursor()
    c.execute("SELECT * FROM bookings WHERE customerId = %s", (customerId,))
    ret = [x for x in c]
    c.close()
    return ret


def deleteBooking(bookingId, customerId):
    c = conn.cursor()
    c.execute("DELETE FROM bookings WHERE bookingId = %s AND customerId = %s", (bookingId, customerId))
    rows_deleted = c.rowcount
    c.close()
    return bool(rows_deleted)

def getLastBookingNumber():
    c = conn.cursor()
    c.execute("SELECT bookingId FROM bookings ORDER BY bookingId DESC LIMIT 1")

    if c.rowcount == 0:
        return 0
    else:
        ret = c.fetchone()[0]
        c.close()
        return ret


# Airports, Flights, Routing
def getAirports():
    c = conn.cursor()
    c.execute("SELECT * FROM airports")
    ret = c.fetchall()
    ret = list(map(lambda t: {
            "airportId" : t[0],
            "name": t[1],
            "country": t[2],
            "state": t[3],
            }, ret))
    c.close()
    return ret

def getAirlines():
    c = conn.cursor()
    c.execute("SELECT * FROM airlines")
    ret = [x for x in c]
    c.close()
    return ret

# Get flights coming out of an airport:
def getFlights(departAirportId, departTime, latestDepart):
    # Finding within 1 hour
    c = conn.cursor()
    c.execute("""
        SELECT *
        FROM flights
        WHERE departAirportId = %s
        AND departTime BETWEEN %s AND %s
        ORDER BY arriveTime ASC""", (departAirportId, departTime, latestDepart))

    ret = [x for x in c]
    c.close()
    return ret


def getFlightPrice(flightId):
    c = conn.cursor()
    c.execute("""
        SELECT economyPrice, firstClassPrice
        FROM prices
        WHERE flightId = %s
        ORDER BY ts DESC
        """, (flightId,))
    ret = [x for x in c]
    c.close()
    return ret


def getFlightInfo(flightId):
    c = conn.cursor()
    c.execute("""
    SELECT *
    FROM flights
    WHERE flightId = %s""", (flightId,))
    ret = c.fetchone()
    c.close()
    return ret

# Insert dummy data:

def addAirport(airportId, name, country, state):
    c = conn.cursor()
    c.execute("INSERT INTO airports VALUES (%s, %s, %s, %s)", (airportId, name, country, state))
    c.close()

def addAirline(airlineId, name, country):
    c = conn.cursor()
    c.execute("INSERT INTO airlines VALUES (%s, %s, %s)", (airlineId, name, country))
    c.close()

def addFlight(flightId, airlineId, departAirportId, arriveAirportId, flightNumber, departTime, arriveTime, economySeats, firstClassSeats):
    c = conn.cursor()
    c.execute("INSERT INTO flights VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (flightId, airlineId, departAirportId, arriveAirportId, flightNumber, departTime, arriveTime, economySeats, firstClassSeats))
    c.close()

def addPrice(flightId, economyPrice, firstClassPrice, ts):
    c = conn.cursor()
    c.execute("INSERT INTO prices VALUES (%s, %s, %s, %s)", (flightId, economyPrice, firstClassPrice, ts))
    c.close()

 # Add a new credit card
def addCreditCard(cardId, customerId, addressId, cardNumber, expiration, nameOnCard, cvcCode):
    c = conn.cursor()
    c.execute ("INSERT INTO customerCreditCards VALUES (%s, %s, %s, %s, %s, %s, %s)",(
        cardId,
        customerId,
        addressId,
        cardNumber,
        expiration,
        nameOnCard,
        cvcCode)
    )
    c.close()
    return True

def getLastCreditCardNumber():
    c = conn.cursor()
    c.execute("SELECT cardId FROM customerCreditCards ORDER BY cardId DESC LIMIT 1")

    if c.rowcount == 0:
        return 0
    else:
        ret = c.fetchone()[0]
        c.close()
        return ret

# Delete credit card
def deleteCreditCard (cardId, customerId):
    c = conn.cursor()
    c.execute("DELETE FROM customerCreditCards WHERE cardId = %s AND customerId = %s", (cardId, customerId))
    rows_deleted = c.rowcount
    c.close()
    return bool(rows_deleted)


def getCreditCards(customerId):
    c = conn.cursor()
    c.execute("SELECT cardId, addressId, cardNumber, expiration, nameOnCard, cvcCode FROM creditCard WHERE customerId=%sl", (customerId, ))
    ret = c.fetchall()
    c.close()

    ret = list(map(lambda t: {
        "cardId" : t[0],
        'addressId' : t[1],
        'cardNumber' : t[2],
        'expiration' : t[3],
        'nameOnCard' : t[4],
        'cvcCode' : t[5],
    }, ret))

    return ret
