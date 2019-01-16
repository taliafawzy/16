import csv
import urllib.request
from cs50 import SQL


from flask import redirect, render_template, request, session
from functools import wraps

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///16.db")


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



def tried_recipe(recipe):

    # update amount of recipes tried in portfolio
    db.execute("UPDATE portfolio SET tried = :tried WHERE userid = :userid", tried=+1, userid = session["userid"])

    # update boolean 'tried' in cookbook
    db.execute("UPDATE cookbook SET tried = :tried WHERE userid = :userid", tried = True, userid = session["userid"])


def save_recipe(recipe):
    # update amount of recipes saved in portfolio
    db.execute("UPDATE portfolio SET saved = :saved WHERE userid = :userid", saved=+1, userid = session["userid"])

    # register recipe into cookbook
    db.execute("INSERT INTO cookbook (recipe, link, tried, rated) VALUES(:recipe, :link, :tried, :rated) WHERE userid = :userid", recipe = recipe, link = link, tried = False, rated = 0, userid = session["userid"])


def personal_rating(rating):
    # update rating of recipe in cookbook
    db.execute("UPDATE cookbook SET rated =:rated WHERE userid = :userid", rated = rating, userid = session["userid"])


def common_rating(single_rating):
    # update rating of recipe in recipe
    db.execute("UPDATE recipe SET rating = :rating / :people AND people = :people WHERE userid = :userid", rating = rating + single_rating, people=+1, userid = session["userid"])








