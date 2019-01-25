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

def delete_recipe(recipe):

    # delete recipe from cookbook
    db.execute("DELETE FROM cookbook WHERE recipe = :recipe AND userid = :userid", recipe = recipe, userid = session["userid"])

    # update amount of recipes saved in portfolio
    db.execute("UPDATE portfolio SET saved = saved - 1 WHERE userid = :userid", userid = session["userid"])

    return delete_recipe

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

def related_recipes(recipe):
    """Returns recipes that were also saved by people who saved visited recipe."""
    # get recipeid from recipe that is being visited
    recipeid = db.execute("SELECT id FROM recipe WHERE recipe = :recipe", recipe = recipe['name'])

    # check what users stored this recipe in cookbook
    related_users = db.execute("SELECT userid FROM cookbook WHERE recipeid = :recipeid", recipeid = recipeid[0]['id'])

    # if any users saved this recipe, check what other recipes they have
    if len(related_users) > 1:
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

        if len(final_related_recipes) == 1:
            final_related_recipes = random.sample(set(final_related_recipes), 1)
            return final_related_recipes
        else:
            # pick two random recipes out of set from recipes
            final_related_recipes = random.sample(set(final_related_recipes), 2)
            return final_related_recipes

    else:
        return None

def checklist():
    # open csv file to retrieve data
    with open('ingredientslist.csv', newline='') as csvfile:

        # seperate data in rows
        rows = csv.reader(csvfile, delimiter=',')

        # create empty list for every category
        fishlist = []
        meatlist = []
        dairylist = []
        vegetablelist = []
        fruitlist = []

        # check category and store ingredient in correct categorylist
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


        return sorted(fishlist), sorted(vegetablelist), sorted(dairylist), sorted(meatlist), sorted(fruitlist)
