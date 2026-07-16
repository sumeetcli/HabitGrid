from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps
from flask_session import Session
import datetime
from helpers import login_required, get_db, generate_heatmap

# session ->  user side session
# Session from flask_session for server side session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
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
        habits_list.append(habit_dict)
    
    db.close()
    return render_template("home.html", habits=habits_list)

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
    db.execute("insert into habits (user_id, name, created_at) values (?, ?, ?)", (session["user_id"], name,today))
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

@app.route("/log", methods=["POST"])
@login_required
def log_habit():
    data = request.get_json()
    dateString = data.get("date")
    habitId = data.get("habitId")
    
    #print(data)
    #print(dateString)

    db = get_db()
    db.execute("insert into habit_logs (habit_id, date, done) values (?, ?, ?)", (habitId,dateString, 1))
    db.commit()
    db.close()

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password") # todo: make this more secure like username input
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

    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method != "POST":
        return render_template("login.html")
    
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        flash("Username or password cannot be empty")
        return redirect("/login")

    db = get_db()
    tableRow = db.execute("select * from users where username = ?", (username,)).fetchone() # unique username makes it easier
    db.close()

    if not tableRow:
        flash("Invalid username & password")
        return redirect("/login")

    if not check_password_hash(tableRow["hash"], password):
        flash("Invalid username & password")
        return redirect("/login")

    session["user_id"] = tableRow["id"]
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)