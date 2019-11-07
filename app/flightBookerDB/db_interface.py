import psycopg2

conn = psycopg2.connect(dbname='flights425', user='postgres', password='space')
conn.autocommit = True
from app.auth import hashPassword



def checkEmail(email):  # Returns True if email not in DB, False if it is.
    c = conn.cursor()
    for row in c.execute("SELECT email FROM customer WHERE email LIKE ?", (email,)):
        c.close()
        return False
    c.close()
    return True


def addCustomerAddress(customerId, line1, line2, postalCode, city, state, country):
    c = conn.cursor()
    c.execute("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?)", (
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


def getCustomerAddresses(customerId):
    c = conn.cursor()
    ret = list(c.execute("SELECT * FROM customerAddresses WHERE customerId = ?", customerId))
    c.close()
    return ret



def deleteCustomerAddress(addressId, customerId):
    c = conn.cursor()
    c.execute("DELETE FROM customerAddresses WHERE addressId = ? AND customerId = ?", (addressId, customerId))
    rows_deleted = c.rowcount
    return bool(rows_deleted)


def createBooking(flightId, customerId):
    c = con.cursor()
    c.execute(" INSERT INTO bookings VALUE(?,?)", (
            customerId,
            flightId)
    )
    c.close()
    return True


def getBooking(customerId):
    c = conn.cursor()
    ret = list(c.execute("SELECT * FROM bookings WHERE customerId = ?", customerId))
    c.close()
    return ret

def deleteBooking(bookingId):
    c = conn.cursor()
    c.execute("DELETE FROM bookings WHERE bookingId = ?", bookingId)
    rows_deleted = c.rowcount
    c.close()
    return bool(rows_deleted)


# Airports, Flights, Routing
def getAirports():
    c = conn.cursor()
    ret = list(c.execute("SELECT * FROM airports"))
    c.close()
    return ret


# Get flights coming out of an airport:
def getFlights(departAirportId, departTime):
    c = conn.cursor()
    ret = list(c.execute("""
        SELECT *
        FROM flights
        WHERE departAirportId = ?
        AND departTime > ?
        ORDER BY arriveTime ASC"""), (departAirportId, departTime))
    c.close()

# Insert dummy data:

def addAirport(airportId, name, country, state):
    c = conn.cursor()
    c.execute("INSERT INTO airports VALUES (?, ?, ?, ?)", (airportId, name, country, state))
    c.close()

def addAirline(airlineId, name, country):
    c = conn.cursor()
    c.execute("INSERT INTO airlines VALUES (?, ?, ?)", (airlineId, name, country))
    c.close()

def addFlight(flightId, airlineId, departAirportId, arriveAirportId, flightNumber, flightDate, departTime, arriveTime, economySeats, firstClassSeats):
    c = conn.cursor()
    c.execute("INSERT INTO flights VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (flightId, airlineId, departAirportId, arriveAirportId, flightNumber, flightDate, departTime, arriveTime, economySeats, firstClassSeats))
    c.close()

def addPrice(flightId, economyPrice, firstClassPrice, ts):
    c = conn.cursor()
    c.execute("INSERT INTO flights VALUES (?, ?, ?, ?)", (flightId, economyPrice, firstClassPrice, ts))
    c.close()
