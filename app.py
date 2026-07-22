from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
# SQLite3 database module: https://docs.python.org/3/library/sqlite3.html
import sqlite3
# functools.wraps decorator: https://docs.python.org/3/library/functools.html#functools.wraps
from functools import wraps
from flask_session import Session
# datetime for date handling: https://docs.python.org/3/library/datetime.html
import datetime
from helpers import login_required, get_db, generate_heatmap, get_streak

# used the following sources for help:
# 1. freecodecamp flask crash course
# 2. kevin powell css youtube tutorials
# 3. Coding2GO css youtube tutorials
# AI citation: Asked AI about how to structure a minimal Flask habit tracker project and session handling.

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "9f7d5b1c3e8a4f6b2d1a7c9e5f8b3d6a0c4e7f1b9a2d5c8e6f3a1b7d9c4e2f8"
# a random secret key, needed for flash() to work
Session(app)

@app.route("/")
@login_required
def home():
    db = get_db()

    habits = db.execute("select * from habits where user_id = ?", (session["user_id"],)).fetchall()
    
    habits_list = []
    for habit in habits:
        habit_dict = dict(habit)
        habit_dict['heatmap'] = generate_heatmap(habit['id'])
        habit_dict['current_streak'] = get_streak(habit['id'])
        habits_list.append(habit_dict)
    
    db.close()

    return render_template("home.html", habits=habits_list)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/habit/add", methods=["POST"])
@login_required
def add_habit():
    name = request.form.get("name")
    #print(name)
    if name == None:
        flash("Habit name cannot be empty")
        return redirect("/")
    
    db = get_db()
    today = datetime.date.today().isoformat() # return string instead of object, "YYYY-MM-DD"
    db.execute("insert into habits (user_id, name) values (?, ?)", (session["user_id"], name))
    db.commit()
    db.close()
    
    return redirect("/")

@app.route("/habit/delete/<int:habit_id>", methods=["POST"])
@login_required
def delete_habit(habit_id):
    db = get_db()
    db.execute("delete from habits where id = ?", (habit_id,))
    db.commit()
    db.close()
    
    return redirect("/")

@app.route("/habit/clear/<int:habit_id>", methods=["POST"])
@login_required
def clear_habit(habit_id):
    db = get_db()
    db.execute("delete from habit_logs where habit_id = ?", (habit_id,))
    db.commit()
    db.close()

    return redirect("/")

@app.route("/log", methods=["POST"])
@login_required
def log_habit():
    data = request.get_json()
    dateString = data.get("date")
    habitId = data.get("habitId")
    
    #print(data)
    #print(dateString)
    #print(habitId)

    db = get_db()

    # check if already logged for this day
    existing = db.execute("select id, done from habit_logs where habit_id = ? and date = ?", (habitId, dateString)).fetchone()
    
    if existing:
        # toggle done value
        new_done = 1 - existing["done"]
        db.execute("update habit_logs set done = ? where habit_id = ? and date = ?", (new_done, habitId, dateString))
    else:
        # not exists so add new row
        db.execute("insert into habit_logs (habit_id, date, done) values (?, ?, ?)", (habitId, dateString, 1))

    db.commit()
    db.close()

    return "Logged"

@app.route("/register", methods=["GET", "POST"])
def register():
    #session.clear()
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password") # todo: think of ways to make auth more secure
    confirmation = request.form.get("confirmation")

    if not username or not password:
        flash("Username or password cannot be empty")
        return redirect("/register")
    if not confirmation:
        flash("You must confirm your password")
        return redirect("/register")
    if password != confirmation:
        flash("Password must match confirm password")
        return redirect("/register")

    db = get_db()
    tableRows = db.execute("select * from users where username = ?", (username,)).fetchone()
    # doesnt work like cs50 sql, sqlite3 needs to fetchall() or fetchone()
    # note: values need to passed as a tuple for python's sqlite3

    if tableRows:
        flash("Username already taken")
        db.close()
        return redirect("/register")

    db.execute("insert into users (username, hash) values (?, ?)", (username, generate_password_hash(password)))

    db.commit()
    db.close()

    session.clear()
    
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    #session.clear()
    if request.method != "POST":
        return render_template("login.html")
    
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        #print("flashing")
        flash("Username or password cannot be empty")
        return redirect("/login")

    db = get_db()
    tableRow = db.execute("select * from users where username = ?", (username,)).fetchone() # unique username makes it easier
    db.close()

    if not tableRow:
        #print("flashing invalid")
        flash("Invalid username & password")
        return redirect("/login")

    if not check_password_hash(tableRow["hash"], password):
        flash("Invalid username & password")
        return redirect("/login")

    session.clear()
    session["user_id"] = tableRow["id"]
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()

    return redirect("/login")


@app.route("/flash-test")
def flash_test():
    flash("It works!")
    return redirect("/login")

if __name__ == "__main__": # so that any import of this python file doesnt start the server
    #app.run(debug=True)
    app.run(debug=False)