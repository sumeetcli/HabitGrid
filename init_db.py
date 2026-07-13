import sqlite3

db = sqlite3.connect("habits.db")

# query to create schema of the db
with open("schema.sql") as f:
    db.executescript(f.read())

db.commit()
db.close()