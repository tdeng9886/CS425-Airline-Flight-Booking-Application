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
