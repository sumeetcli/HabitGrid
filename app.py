from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps
from flask_session import Session
import datetime

# session from flask for user side session
# Session from flask_session for server side session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

life_expectancy = 73

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_db():
    db = sqlite3.connect("habits.db")
    db.row_factory = sqlite3.Row # imp: dictionary outputs, easier to access than tuple
    return db

@app.route("/")
@login_required
def home():
    db = get_db()
    tableRow = db.execute("select dob from settings where user_id = ?", (session["user_id"],)).fetchone()

    if not tableRow:
        db.close()
        return render_template("home.html", has_dob=False)

    dobData = tableRow["dob"]

    if dobData == None:
        db.close()
        return render_template("home.html", has_dob=False)
    
    year, month, day = dobData.split("-")
    dob = datetime.date(int(year), int(month), int(day))

    days_lived = (datetime.date.today() - dob).days
    total = life_expectancy * 365
    weeks = days_lived // 7
    total_weeks = total // 7

    db.close()

    return render_template("home.html", has_dob=True, days_lived=days_lived, total=total, weeks = weeks, total_weeks = total_weeks, life_expectancy=life_expectancy)

@app.route("/habits", methods=["GET", "POST"])
@login_required
def habits():
    db = get_db()

    if request.method == "POST":
        name = request.form.get("name")

        if name == None:
            flash("Habit name cannot be empty")
            db.close()
            return redirect("/habits")

        db.execute("insert into habits (user_id, name) values (?, ?)", (session["user_id"], name))
        db.commit()
        db.close()
        return redirect("/habits")

    habitsList = db.execute("select * from habits where user_id = ?", (session["user_id"],)).fetchall()
    db.close()

    return render_template("habits.html", habits=habitsList)

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
    elif not confirmation:
        flash("You must confirm your password")
        return redirect("/register")
    elif password != confirmation:
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

    user_id = db.execute("select id from users where username = ?", (username,)).fetchone()["id"]

    db.execute("insert into settings (user_id) values (?)", (user_id,))

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

@app.route("/set_dob", methods = ["POST"])
def set_dob():
    dob = request.form.get("dob")
    db = get_db()
    db.execute("update settings set dob = ? where user_id = ?", (dob, session["user_id"]))
    db.commit()
    db.close()
    return redirect("/")                                                                   

if __name__ == "__main__":
    app.run(debug=True)