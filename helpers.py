from functools import wraps
import sqlite3
from flask import session, redirect
import datetime

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

def generate_heatmap(habit_id):
    today = datetime.date.today()
    year_start = datetime.date(today.year, 1, 1)
    
    heatmap = []
    week = []
    
    for i in range(365):
        date = year_start + datetime.timedelta(days=i)
        week.append({"date": date.isoformat(), "done": 0})
        
        # weekly
        if len(week) == 7:
            heatmap.append(week)
            week = []
    
    return heatmap