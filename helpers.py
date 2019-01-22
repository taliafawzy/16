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
    db.execute("UPDATE portfolio SET tried = tried + 1 WHERE userid = :userid", userid = session["userid"])

    # update boolean 'tried' in cookbook
    tried = db.execute("UPDATE cookbook SET tried = 1 WHERE userid = :userid AND recipe = :recipe", userid = session["userid"], recipe = recipe)

    return tried

def save_recipe(recipe):
    """Updates amount of recipes saved in portfolio and inserts recipe into cookbook."""

    # update amount of recipes saved in portfolio
    db.execute("UPDATE portfolio SET saved = saved + 1 WHERE userid = :userid", userid = session["userid"])

    # get recipeid
    recipeid = db.execute("SELECT id FROM recipe WHERE recipe = :recipe", recipe = recipe["name"])
    recipeid = recipeid[0]['id']

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
    # get recipeid from recipe that is being visited
    recipeid = db.execute("SELECT id FROM recipe WHERE recipe = :recipe", recipe = recipe['name'])

    # check what users stored this recipe in cookbook
    related_users = db.execute("SELECT userid FROM cookbook WHERE recipeid = :recipeid", recipeid = recipeid[0]['id'])

    # if any users saved this recipe, check what other recipes they have
    if len(related_users) != 0:
        related_users_list = [x['userid'] for x in related_users]
        related_recipes = []
        for user in related_users_list:
            related_recipes_from_users = db.execute("SELECT recipe FROM cookbook WHERE userid = :userid", userid = user)
            related_recipes.append(related_recipes_from_users)

        # make list out of recipes from all users together
        related_recipes = [x['recipe'] for x in related_recipes for x in x]

        # make name of visited recipe into string and place into empty list
        recipename = []
        for letter in recipe['name']:
             recipename.append(letter)
        recipe = ''.join(recipename)

        # make list out of recipes from all users together minus visited recipe
        final_related_recipes = [item for item in related_recipes if item not in recipe]

        # pick two random recipes out of set from recipes
        final_related_recipes = random.sample(set(final_related_recipes), 2)
        return final_related_recipes
    else:
        return None

def checklist():
    with open('ingredientslist.csv', newline='') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        fishlist = []
        meatlist = []
        dairylist = []
        vegetablelist = []
        fruitlist = []
        for row in rows:
            if row[0] == 'fish & seafood':
                fishlist.append(row[1])
            elif row[0] == 'dairy':
                dairylist.append(row[1])
            elif row[0] == 'meat':
                meatlist.append(row[1])
            elif row[0] == 'fruit':
                fruitlist.append(row[1])
            elif row[0] == 'vegetables':
                vegetablelist.append(row[1])
        return fishlist, vegetablelist, dairylist, meatlist, fruitlist
