from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
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

#@app.route("/testregister")
#def testregister():

    # redirect user to login form
 #   return render_template("testregister.html")

@app.route("/checkname", methods = ["GET"])
def checkname():

    username = request.args.get('name')
    print(username)

    # query database for username
    userdata = db.execute("SELECT * FROM userdata WHERE username = :username", username=username)

    # ensure username exists and password is correct
    if len(userdata) == 1:
        result = "username already exists"
        return jsonify(result = result)
    else:
        result = "username does not exist yet"
        return jsonify(result=result)



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
        if not request.form.get("name"):
            return apology("must provide username")
        elif not (request.form.get("password") or request.form.get("confirmation")):
            return apology("must provide password")

        # ensure password and passwordcheck match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password does not match")

        # query database for username
        userdata = db.execute("SELECT * FROM userdata WHERE username = :username", username=request.form.get("name"))

        # ensure username exists and password is correct
        if len(userdata) == 1:
            return apology("username already exists")

        # encrypt password
        myctx = CryptContext(schemes=["sha256_crypt"], sha256_crypt__default_rounds=80000)
        hash = myctx.hash(request.form.get("password"))

        # insert user/password into userdata
        userdata = db.execute("INSERT INTO userdata (username, hash) VALUES (:username, :hash)",username=request.form.get("name"), hash=hash)

        # query database for username
        userdata = db.execute("SELECT * FROM userdata WHERE username = :username", username=request.form.get("name"))

        # remember wich user has logged in
        session["userid"] = userdata[0]["id"]

        # create portfolio
        db.execute("CREATE TABLE if not exists portfolio ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'userid' INTEGER, 'tried' INTEGER, 'saved' INTEGER, 'rated' INTEGER, FOREIGN KEY(userid) REFERENCES userdata(id))")

        # update portfolio
        db.execute("INSERT INTO portfolio (userid,tried, saved, rated) VALUES(:userid, 0,0,0)", userid = session["userid"])

        # create cookbook
        db.execute("CREATE TABLE if not exists cookbook ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'userid' INTEGER, 'recipeid' INTEGER, 'recipe' TEXT, 'link' TEXT, 'tried' BOOLEAN, 'rated' INTEGER, FOREIGN KEY(userid) REFERENCES userdata(id), FOREIGN KEY(recipeid) REFERENCES recipe(id))")


        return redirect(url_for("homepage"))

    else:
        return render_template("register.html")

@app.route("/mypage", methods = ["GET", "POST"])
@login_required
def mypage():

    # query database to see what user is visiting their page and retrieve their data
    user = db.execute("SELECT username FROM userdata WHERE id = :id", id = session["userid"])
    user = user[0]["username"]
    portfolio = db.execute("SELECT * FROM portfolio WHERE userid = :userid", userid = session["userid"])
    tried = portfolio[0]["tried"]
    saved = portfolio[0]["saved"]
    rated = portfolio[0]["rated"]

    # query database to retrieve cookbook from user
    cookbook = db.execute("SELECT * FROM cookbook WHERE userid = :userid", userid = session["userid"])

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # if user clicks on delete button
        if "delete" in request.form:

            # store the delete button that is being clicked on
            recipe = request.form.get("delete")

            # use helpersfunction to update database
            recipe = delete_recipe(recipe)

            # render updated cookbook
            cookbook = db.execute("SELECT * FROM cookbook WHERE userid = :userid", userid = session["userid"])

            return render_template("mypage.html", user = user, tried = tried, saved = saved, cookbook=cookbook)


        # if user clicks on tried button
        if "tried" in request.form:
            # store the tried button that is being clicked on
            recipe = request.form.get("tried")

            # use helpersfunction to update database
            recipe = tried_recipe(recipe)

            # render updated cookbook
            cookbook = db.execute("SELECT * FROM cookbook WHERE userid = :userid", userid = session["userid"])

            return render_template("mypage.html", user = user, tried = tried, saved = saved, cookbook=cookbook)

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("mypage.html", user = user, tried = tried, saved = saved, cookbook=cookbook)

@app.route("/", methods = ["GET"])
@app.route("/index", methods = ["GET"])
def root():
    return redirect(url_for("homepage"))


@app.route("/homepage", methods = ["GET", "POST"])
def homepage():

    fishlist, vegetablelist, dairylist, meatlist, fruitlist = checklist()
    render_template("homepage.html", fishlist=fishlist, vegetablelist=vegetablelist, dairylist=dairylist, meatlist=meatlist, fruitlist=fruitlist)

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # check what checkboxes are marked
        if request.form.getlist("ingredient"):
            ingredient = request.form.getlist("ingredient")

            # get results from helpersfunction
            recipelist = getResults(ingredient)

            if len(recipelist) == 0:
                return apology("No recipes found")

            else:
                # store recipelist in session
                session['recipelist'] = recipelist

                # store choice of ingredients in session
                session['choice'] = ingredient

                return redirect(url_for("results"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("homepage.html",  fishlist=fishlist, vegetablelist=vegetablelist, dairylist=dairylist, meatlist=meatlist, fruitlist=fruitlist)

#TODO: error if puppy API gives no results
#TODO: dubbele code in helpersfunctie plaatsen
@app.route("/results", methods = ["GET", "POST"])
def results():

    if request.referrer and request.referrer.endswith("homepage"):
        recipelist = session['recipelist']

        # display the person's choice on ingredients they chose on previous page
        choice = session['choice']
        choice = ','.join(choice)
        recipes = []
        ingredientsSet = set()

        # create a list of dictionaries (1 recipe 1 dictionary) to make a table with images and recipes
        for recipe in recipelist:
            recipeDict = dict.fromkeys(['name', 'picture', 'url'])
            recipeDict['name'] = recipe.strip()
            ingredient = (recipelist[recipe]["ingredients"]).split(',')

            nonChoice = [i.strip() for i in ingredient if i.strip() not in choice]
            print(nonChoice, choice)
            ingredientsSet = nonChoice

            recipeDict['picture'] = recipelist[recipe]["picture"]
            recipeDict['ingredients'] = recipelist[recipe]["ingredients"]
            recipeDict['url'] = recipelist[recipe]["url"]

            recipes.append(recipeDict)

            # check if shown recipes are already in recipe database, if not store them
            recipeDatabase = db.execute("SELECT * FROM recipe WHERE recipe = :recipe", recipe = recipeDict['name'])
            if len(recipeDatabase) == 0:
                db.execute("INSERT INTO recipe (recipe, rating, people) VALUES(:recipe, :rating, :people)", recipe = recipeDict['name'], rating = 0, people = 0)

        # store list of recipes in session
        session['recipes'] = recipes

        return render_template("results.html", choice=choice, recipes = recipes, ingredientsSet = ingredientsSet)

    # if user reached route via POST (as by submitting a form via POST)
    elif request.referrer and request.referrer.endswith("results") and request.method == "POST":

        # if user clicks on recipe
        if  "submit_button" in request.form:

            # get the recipeName from the form that was just submitted
            recipeName = request.form['submit_button']

            # get the saved recipes list
            recipes = session['recipes']

            # locate our recipe
            recipe = next(item for item in recipes if item["name"] == recipeName)

            # store recipe in session
            session['recipe'] = recipe

            return redirect(url_for("recipe"))

        # if user clicks on extra ingredient
        elif "extra_ingredient_submit_button" in request.form:

            # get previous choice and update it
            choice = session['choice']
            newChoice = request.form['extra_ingredient_submit_button']
            choice.append(newChoice)
            session['choice'] = choice
            print(choice)

            # get new ingredients
            recipelist = getResults(choice)
            if len(recipelist) == 0:
                return apology("No recipes found")
            else:
                recipes = []
                ingredientsSet = set()

                # create a list of dictionaries (1 recipe 1 dictionary) to make a table with images and recipes
                for recipe in recipelist:
                    recipeDict = dict.fromkeys(['name', 'picture', 'url'])
                    recipeDict['name'] = recipe.strip()
                    ingredient = (recipelist[recipe]["ingredients"]).split(',')

                    nonChoice = [i.strip() for i in ingredient if i.strip() not in choice]
                    ingredientsSet = nonChoice

                    recipeDict['picture'] = recipelist[recipe]["picture"]
                    recipeDict['ingredients'] = recipelist[recipe]["ingredients"]
                    recipeDict['url'] = recipelist[recipe]["url"]
                    recipes.append(recipeDict)

                    # check if shown recipes are already in recipe database, if not store them
                    recipeDatabase = db.execute("SELECT * FROM recipe WHERE recipe = :recipe", recipe = recipeDict['name'])
                    if len(recipeDatabase) == 0:
                        db.execute("INSERT INTO recipe (recipe, rating, people) VALUES(:recipe, :rating, :people)", recipe = recipeDict['name'], rating = 0, people = 0)

                # store list of recipes in session
                session['recipes'] = recipes

                return render_template("results.html", choice=','.join(choice), recipes = recipes, ingredientsSet = ingredientsSet)




@app.route("/recipe", methods = ["GET", "POST"])
def recipe():
    # retrieve recipe that was previously stored in session
    recipe = session['recipe']

    # check if user already saved this recipe for the notsaved flag that is used in the recipe.html
    notsaved = False
    if "userid" in session:
        saved_recipe = db.execute("SELECT recipe FROM cookbook WHERE userid = :userid and recipe = :name", userid = session["userid"], name = recipe["name"])
        if not saved_recipe:
            notsaved = True
        else:
            notsaved = False

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":


        if request.form.get("save_recipe"):
            recipe = save_recipe(recipe)
            return redirect(url_for("recipe"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:

        # check if there are recipes related to recipe that is visited
        related = related_recipes(recipe)

        # if there are related recipes, retrieve url from recipe
        if related is not None:
            urls = []
            for item in related:
                url = db.execute("SELECT link FROM cookbook WHERE recipe = :item", item = item)
                urls.append(url)
            urls = [url['link'] for url in urls for url in url]

            # zip name of recipenames and recipe urls into one list
            related_zip = zip(related, urls)

            return render_template("recipe.html", recipe = recipe, related=related, related_zip = related_zip, notsaved = notsaved)

        # if there are no related recipes, no related recipes table is shown
        else:
            return render_template("recipe.html", recipe = recipe, notsaved = notsaved)
