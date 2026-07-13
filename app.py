from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps
from flask_session import Session

# session from flask for user side session
# Session from flask_session for server side session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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
    return "HabitGrid"

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

    db.execute("insert into users (username, hash) values (?,?)", (username, generate_password_hash(password)))
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

if __name__ == "__main__":
    app.run(debug=True)