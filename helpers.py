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
    
    # initialize schema if needed
    with open("schema.sql") as f:
        db.executescript(f.read())
    
    return db

def generate_heatmap(habit_id):
    db = get_db()
    
    today = datetime.date.today()
    year_start = datetime.date(today.year, 1, 1)
    #print(datetime.timezone())
    today_str = today.isoformat()
    
    logs = db.execute("select date, done from habit_logs where habit_id = ?", (habit_id,)).fetchall()
    db.close()
    
    heatmap = []
    week = []
    
    for i in range(365):
        date = year_start + datetime.timedelta(days=i)
        dateString = date.isoformat()
        month = date.month
        
        # setting the days that were already done
        done = 0
        for log in logs:
            if log[0] == dateString:
                done = log[1]
        
        is_today = dateString == today_str
        is_future = dateString > today_str
        
        # week.append({"date": dateString, "done": done, "today": is_today})
        #week.append({"date": dateString, "done": done, "today": is_today, "future": is_future})
        #color = 
        #week.append({"date": dateString, "done": done, "today": is_today, "future": is_future, "color": color})
        week.append({"date": dateString, "done": done, "today": is_today, "future": is_future, "month": month})
        
        if len(week) == 7:
            heatmap.append(week)
            week = []
    
    return heatmap

def get_streak(habit_id):
    db = get_db()
    today = datetime.date.today()
    
    logs = db.execute("select date, done from habit_logs where habit_id = ? order by date desc", (habit_id,)).fetchall()
    db.close()
    
    streak = 0
    for x in logs:
        if x["done"] == 1:
            streak += 1
        else:
            if x["done"] == 0:
                break
    
    return streak