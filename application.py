from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from passlib.context import CryptContext
from helpers import *
from puppy import *

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
db = SQL("sqlite:///16.db")


@app.route("/login", methods=["GET", "POST"])
def login():

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure pasword and username is submitted
        if not request.form.get("username"):
            return apology("must provide username")
        elif not request.form.get("password"):
            return apology("must provide password")

        # create user database
        userdata = db.execute("SELECT * FROM userdata WHERE username = :username", username = request.form.get("username"))

        # ensure username exists and password is correct
        if len(userdata) != 1 or not pwd_context.verify(request.form.get("password"), userdata[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["userid"] = userdata[0]["id"]

        # redirect user to home page
        return redirect(url_for("homepage"))

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
        userdata = db.execute("SELECT * FROM userdata WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(userdata) == 1:
            return apology("username already exists")

        # encrypt password
        myctx = CryptContext(schemes=["sha256_crypt"], sha256_crypt__default_rounds=80000)
        hash = myctx.hash(request.form.get("password"))

        # insert user/password into userdata
        userdata = db.execute("INSERT INTO userdata (username, hash) VALUES (:username, :hash)",username=request.form.get("username"), hash=hash)

        # create portfolio
        db.execute("CREATE TABLE if not exists portfolio ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'userid' INTEGER, 'tried' INTEGER, 'saved' INTEGER, 'rated' INTEGER, FOREIGN KEY(userid) REFERENCES userdata(id))")

        # create cookbook
        db.execute("CREATE TABLE if not exists cookbook ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'userid' INTEGER, 'recipeid' INTEGER, 'recipe' TEXT, 'link' TEXT, 'tried' BOOLEAN, 'rated' INTEGER, FOREIGN KEY(userid) REFERENCES userdata(id), FOREIGN KEY(recipeid) REFERENCES recipe(id))")

        # remember wich user has logged in
        session["userid"] = userdata[0]["id"]


        return redirect(url_for("homepage"))

    else:
        return render_template("register.html")

@app.route("/mypage", methods = ["GET", "POST"])
@login_required
def mypage():
    if request.method == "POST":

        portfolio = db.execute("SELECT * FROM portfolio WHERE userid = :userid", userid = session["userid"])
        name = portfolio[0]["username"]
        tried = portfolio[0]["tried"]
        saved = portfolio[0]["saved"]
        rated = portfolio[0]["rated"]

        if request.form.get("rated"):
            rating = db.execute("SELECT rating FROM cookbook WHERE rated = :rated AND userid = :userid", rated = request.form.get("rated"), userid = session["userid"])
            rating = personal_rating(rating)

        if request.form.get("tried"):
            recipe = db.execute("SELECT recipe FROM cookbook WHERE tried = :tried AND userid = :userid", tried = request.form.get("tried"), userid = session["userid"])
            recipe = tried_recipe(recipe)

        return render_template("mypage.html", tried=tried, saved=saved, rated=rated)

    else:
        return render_template("mypage.html")

@app.route("/homepage", methods = ["GET", "POST"])
def homepage():
    if request.method == "POST":
        if request.form.getlist("ingredient"):
            ingredient = request.form.getlist("ingredient")
            recipelist = getResults(ingredient)
            session['recipelist'] = recipelist
            session['choice'] = ingredient
            return redirect(url_for("results"))
    else:
        return render_template("homepage.html")

#TODO: error if puppy API gives no results
@app.route("/results", methods = ["GET", "POST"])
def results():
    if request.referrer and request.referrer.endswith("homepage"):
        recipelist = session['recipelist']
        #we need choice to display the person what ingredients they chose on previous page
        choice = session['choice']
        choice = ','.join(choice)
        recipes = []
        ingredientsSet = set()
        #we create a list of dictionaries (1 recipe 1 dictionary) to make a table with images and recipes
        for recipe in recipelist:
            recipeDict = dict.fromkeys(['name', 'picture', 'url'])
            recipeDict['name'] = recipe.strip()
            ingredient = (recipelist[recipe]["ingredients"]).split(',')
            for food in ingredient:
                ingredientsSet.add(food.strip())
            recipeDict['picture'] = recipelist[recipe]["picture"]
            recipeDict['ingredients'] = recipelist[recipe]["ingredients"]
            recipeDict['url'] = recipelist[recipe]["url"]
            recipes.append(recipeDict)
        session['recipes'] = recipes

        return render_template("results.html", choice=choice, recipes = recipes, ingredientsSet = ingredientsSet)
    elif request.referrer and request.referrer.endswith("results") and request.method == "POST":
        if  "submit_button" in request.form:
            #get the recipeName from the form that was just submitted
            recipeName = request.form['submit_button']
            #get the saved recipes list
            recipes = session['recipes']
            #locate our recipe
            recipe = next(item for item in recipes if item["name"] == recipeName)
            session['recipe'] = recipe
            return redirect(url_for("recipe"))
        elif "extra_ingredient_submit_button" in request.form:
            #get previous choice and update it
            choice = session['choice']
            newChoice = request.form['extra_ingredient_submit_button']
            choice.append(newChoice)
            session['choice'] = choice
            #get new ingredients
            recipelist = getResults(choice)
            recipes = []
            ingredientsSet = set()
            #we create a list of dictionaries (1 recipe 1 dictionary) to make a table with images and recipes
            for recipe in recipelist:
                recipeDict = dict.fromkeys(['name', 'picture', 'url'])
                recipeDict['name'] = recipe.strip()
                ingredient = (recipelist[recipe]["ingredients"]).split(',')
                for food in ingredient:
                    ingredientsSet.add(food.strip())
                recipeDict['picture'] = recipelist[recipe]["picture"]
                recipeDict['ingredients'] = recipelist[recipe]["ingredients"]
                recipeDict['url'] = recipelist[recipe]["url"]
                recipes.append(recipeDict)
            session['recipes'] = recipes

            return render_template("results.html", choice=','.join(choice), recipes = recipes, ingredientsSet = ingredientsSet)




@app.route("/recipe", methods = ["GET", "POST"])
def recipe():
    recipe = session['recipe']

    if request.method == "POST":
        if request.form.get("save"):
            recipe = save_recipe(recipe)
        return render_template("recipe.html", recipe = recipe)
    else:
        return render_template("recipe.html", recipe = recipe)
