from os import urandom

key = urandom(16).hex()
SECRET_KEY = key
SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"