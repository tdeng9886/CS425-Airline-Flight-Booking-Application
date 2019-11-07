from app.flightBookerDB import db_interface
from string import ascii_letters, digits
from random import choice
import hashlib

'''
incomplete still... :(
'''


pw_salt = "Zm1ha3NsZW5kZmlsIGFlZ2Z1YWhrdXMgZm5qa3NkbmtqdmMgYW5zY3Nham5kY2FucyBkc2puY3NhamRrbmZqbjRxZm52cjM5NA=="

# authtoken == 64 random letters/numbers
def generateToken():
    return ''.join([choice(ascii_letters + digits) for i in range(64)])


# sha512: salt,customerId,password
def hashPassword(customerId, password):
    return hashlib.sha512(','.join([pw_salt, customerId, password])).hexdigest()


def checkUserCreds(email, password):
    c = db_interface.conn.cursor()
    r = c.execute('SELECT customerId, password FROM customers WHERE email = ?', (email, )).fetchone()
    c.close()
    return hashPassword(r['customerId'], password) == r['password']

def loginUser(email, password):
    if (not checkUserCreds(email, password)):
        return [ 'invalid credentials' ]
    c = db_interface.conn.cursor()
    c.execute('UPDATE customers set authToken=? WHERE email=?;', (generateToken(), email ))
    c.close()
    return False


def authUser():
    c = db_interface.conn.cursor()
    token = c.execute('SELECT authToken FROM customers')