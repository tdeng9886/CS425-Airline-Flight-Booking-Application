import psycopg2

conn = psycopg2.connect(dbname='flightBooker', user='flightBooker', password='hunter2')
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
def getFlights(departAirportID, departTime):
    return list(c.execute("""
        SELECT *
        FROM flights
        WHERE departAirportID = ?
        AND departTime > ?
        ORDER BY arriveTime ASC"""), (departAirportID, departTime))
