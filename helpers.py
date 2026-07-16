from functools import wraps
import sqlite3
from flask import session, redirect

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_db():
    db = sqlite3.connect("habits.db")
    db.row_factory = sqlite3.Row
    return db

