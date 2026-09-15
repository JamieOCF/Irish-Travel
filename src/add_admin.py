from werkzeug.security import generate_password_hash
import sqlite3
from sys import argv

username = argv[1]
password = generate_password_hash(argv[2])

db = sqlite3.connect("app.db")
db.execute("INSERT INTO users (username, password, access_level) VALUES (?, ?, ?)", (username, password, 1))
db.commit()
db.close()