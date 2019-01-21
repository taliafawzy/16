import csv
import urllib.request
from cs50 import SQL
import random

from flask import redirect, render_template, request, session
from functools import wraps
from puppy import *

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
        if session.get("userid") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def getResults(ingredient):
    """Looks up recipe with given ingredients from user."""
    puppy = Puppy()
    recipelist = puppy.search_recipe(ingredient)

    return recipelist



def tried_recipe(recipe):
    """Updates amount of recipes tried in portfolio and updates boolean in cookbook."""

    # update amount of recipes tried in portfolio
    db.execute("UPDATE portfolio SET tried = :tried WHERE userid = :userid", tried=+1, userid = session["userid"])

    # update boolean 'tried' in cookbook
    db.execute("UPDATE cookbook SET tried = :tried WHERE userid = :userid", tried = True, userid = session["userid"])

    return tried_recipe

def save_recipe(recipe):
    """Updates amount of recipes saved in portfolio and inserts recipe into cookbook."""

    # update amount of recipes saved in portfolio
    db.execute("UPDATE portfolio SET saved = saved + 1 WHERE userid = :userid", userid = session["userid"])

    cookbook = db.execute("SELECT * FROM recipe")
    print(cookbook)
    # get recipeid
    recipeid = db.execute("SELECT id FROM recipe WHERE recipe = :recipe", recipe = recipe["name"])
    print(recipeid)
    recipeid = recipeid[0]['id']
    print(recipeid)
    # register recipe into cookbook
    saved_recipe = db.execute("INSERT INTO cookbook (userid, recipeid, recipe, link, tried, rated) VALUES(:userid, :recipeid, :recipe, :link, :tried, :rated)", recipeid = recipeid, recipe = recipe['name'], link = recipe["url"], tried = 0, rated = 0, userid = session["userid"])

    return saved_recipe

def personal_rating(rating):
    """Updates rating of recipe in cookbook."""

    # update rating of recipe in cookbook
    db.execute("UPDATE cookbook SET rated =:rated WHERE userid = :userid", rated = rating, userid = session["userid"])

    return personal_rating

def common_rating(single_rating):
    """Updates common rating of a recipe when rated on recipe page."""

    # update rating of recipe in recipe
    db.execute("UPDATE recipe SET rating = :rating / :people AND people = :people WHERE userid = :userid", rating = rating + single_rating, people=+1, userid = session["userid"])

    return common_rating

def related_recipes(recipe):
    """Returns recipes that were also saved by people who saved visited recipe."""

    recipeid = db.execute("SELECT id FROM recipe WHERE recipe = :recipe", recipe = recipe)
    related_users = db.execute("SELECT userid FROM cookbook WHERE recipeid = :recipeid", recipeid = recipeid)
    related_recipes_from_users = db.execute("SELECT recipe FROM cookbook WHERE userid = :userid", userid = related_users)

    random.sample(set(related_recipes_from_users), 2)
