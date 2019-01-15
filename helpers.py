import csv
import urllib.request

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def getResults(keyword):
    """Looks up recipe with given keywords from user."""








@app.route("/tried", methods=["GET", "POST"])
def personaltried():

    # insert into database if recipe clicked "tried"
    db.execute("INSERT INTO portfolio (tried) VALUES (:tried)")

    #sum all tried recipes
    db.execute("SELECT tried, SUM(tried) AS tried, tried FROM portfolio WHERE UserID = :id",  id=session["user_id"])



@app.route("/rated", methods=["GET", "POST"])
def personalrated():

    # insert into database if recipe clicked "rated"
    db.execute("INSERT INTO portfolio (rated) VALUES (:rated)")

    #sum all rated recipes
    db.execute("SELECT rated, SUM(rated) AS rated, rated FROM portfolio WHERE UserID = :id",  id=session["user_id"])



@app.route("/saved", methods=["GET", "POST"])
def personalsaved():

    # insert into database if recipe clicked "saved"
    db.execute("INSERT INTO portfolio (saved) VALUES (:saved)")

    #sum all saved recipes
    db.execute("SELECT saved, SUM(saved) AS saved, saved FROM portfolio WHERE UserID = :id",  id=session["user_id"])


