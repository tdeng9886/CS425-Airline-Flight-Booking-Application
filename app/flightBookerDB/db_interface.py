import psycopg2

conn = psycopg2.connect(dbname='flights425', user='postgres', password='space')
conn.autocommit = True
c = conn.cursor


def createCustomer(name, email, password):
    return c.execute("""
        INSERT INTO customers
        VALUES (?, ?, ?)
        RETURNING customerId""", (name, email, password)).fetchone()


def checkEmail(email):  # Returns True if email not in DB, False if it is.
    for row in c.execute("SELECT email FROM customer WHERE email LIKE ?", (email,)):
        return False
    return True


def addCustomerAddress(customerId, line1, line2, postalCode, city, state, country):
    c.execute("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?)", (
        customerId,
        line1,
        line2,
        postalCode,
        city,
        state,
        country)
    )
    return True


def getCustomerAddresses(customerId):
    return list(c.execute("SELECT * FROM customerAddresses WHERE customerId = ?", customerId))


def deleteCustomerAddress(addressId, customerId):
    c.execute("DELETE FROM customerAddresses WHERE addressId = ? AND customerId = ?", (addressId, customerId))
    rows_deleted = c.rowcount
    return bool(rows_deleted)


def createBooking(flightId, customerId):
    c.execute(" INSERT INTO bookings VALUE(?,?)", (
            customerId,
            flightId)
    )
    return True


def getBooking(customerId):
    return list(c.execute("SELECT * FROM bookings WHERE customerId = ?", customerId))


def deleteBooking(bookingId):
    c.execute("DELETE FROM bookings WHERE bookingId = ?", bookingId)
    rows_deleted = c.rowcount
    return bool(rows_deleted)


# Airports, Flights, Routing
def getAirports():
    return list(c.execute("SELECT * FROM airports"))


# Get flights coming out of an airport:
def getFlights(departAirportId, departTime):
    return list(c.execute("""
        SELECT *
        FROM flights
        WHERE departAirportId = ?
        AND departTime > ?
        ORDER BY arriveTime ASC"""), (departAirportId, departTime))

# Insert data:

def addAirport(airportId, name, country, state):
    c.execute("INSERT INTO airports VALUES (?, ?, ?, ?)", (airportId, name, country, state))

def addAirline(airlineId, name, country):
    c.execute("INSERT INTO airlines VALUES (?, ?, ?)", (airlineId, name, country))

def addFlight(flightId, airlineId, departAirportId, arriveAirportId, flightNumber, flightDate, departTime, arriveTime, economySeats, firstClassSeats):
    c.execute("INSERT INTO flights VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (flightId, airlineId, departAirportId, arriveAirportId, flightNumber, flightDate, departTime, arriveTime, economySeats, firstClassSeats))

def addPrice(flightId, economyPrice, firstClassPrice, ts):
    c.execute("INSERT INTO flights VALUES (?, ?, ?, ?)", (flightId, economyPrice, firstClassPrice, ts))
