from faker import Faker
import random
from datetime import timedelta
import db_interface
faker = Faker()

# faker.date_time_between(start_date='now', end_date='+1y')
# Python datetime objects can be inserted directly into a postgres DB.

def gen_flight_timestamp():
    departTime = faker.date_time_between(start_date='now', end_date='+1y')
    endPoint = departTime + timedelta(days=1)
    arriveTime = faker.date_time_between(start_date=departTime, end_date=endPoint)

    return (departTime, arriveTime)
flights_added = 0
file = open("flights.csv")
for line in file:
    line = line.replace('"', '')
    try:
        row = line.split(",")
        (departTime, arriveTime) = gen_flight_timestamp()
        flightId = random.randint(111111111111, 999999999999)
        airlineId = row[7]
        departAirportId = row[10]
        arriveAirportId = row[11]
        flightNumber = random.randint(111, 999)
        economySeats = random.choice([40, 80, 120, 240])
        firstClassSeats = random.choice([5, 10, 15, 20])

        db_interface.addFlight(flightId, airlineId, departAirportId, arriveAirportId, flightNumber, departTime, arriveTime, economySeats, firstClassSeats)
        flights_added += 1
        if flights_added % 100 == 0:
            print(flights_added)
    except Exception as e:
        print(e)
