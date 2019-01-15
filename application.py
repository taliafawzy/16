from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from passlib.context import CryptContext
from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/login", methods=["GET", "POST"])
def login():

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure pasword and username is submitted
        if not request.form.get("username"):
            return apology("must provide username")
        elif not request.form.get("password")
            return apology("must provide password")

        # create user database
        userdata = db.execute("CREATE TABLE if not exists history('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        'userid' INTEGER, 'username' TEXT, 'hash' TEXT, FOREIGN KEY(userid) REFERENCES users(id))")
        # ensure username exists and password is correct
        if len(userdata) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():

     # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username/pasword/confirmation was submitted
        if not request.form.get("username"):
            return apology("must provide username")
        elif not (request.form.get("password") or request.form.get("confirmation")):
            return apology("must provide password")

        # ensure password and passwordcheck match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password does not match")

        # query database for username
        userdata = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) == 1:
            return apology("username already exists")

        # encrypt password
        myctx = CryptContext(schemes=["sha256_crypt"],
                             sha256_crypt__default_rounds=80000)
        hash = myctx.hash(request.form.get("password"))

        # insert user/password into userdata
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                   username=request.form.get("username"), hash=hash)

        userdata = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        # remember wich user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect(url_for("index"))

    else:
        return render_template("register.html")
