import psycopg2

conn = psycopg2.connect(dbname='flightBooker', user='flightBooker', password='hunter2')
c = conn.cursor


def createCustomer(name, email, password):
    c.execute("INSERT INTO customers VALUES (?, ?, ?)", (name, email, password))
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
