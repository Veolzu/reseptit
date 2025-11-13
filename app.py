import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, flash
import config, users, recipe_book

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return "VIRHE: salasanat eivät ole samat"

        try:
            users.create_user(username, password1)
            flash("Tunnuksen luominen onnistui, voit nyt kirjautua sisään")
            return redirect("/")            
        except sqlite3.IntegrityError:
            return "VIRHE: tunnus on jo varattu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")

@app.route("/new_recipe", methods=["POST"])
def new_recipe():
    title = request.form["title"]
    content = request.form["content"]
    user_id = session["user_id"]
    print(title, content, user_id)
    recipe_id = recipe_book.add_recipe(title, content, user_id)
    return redirect("/recipe/" + str(recipe_id))

@app.route("/new_rating", methods=["POST"])
def new_rating():
    content = request.form["content"]
    user_id = session["user_id"]
    recipe_id = request.form["recipe_id"]
    rating = request.form["dropdown"]
    recipe_book.add_rating(content, rating,  user_id, recipe_id)
    return redirect("/recipe/" + str(recipe_id))

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = recipe_book.get_recipe(recipe_id)
    ratings = recipe_book.get_ratings(recipe_id)
    return render_template("recipe.html", recipe=recipe, ratings=ratings)


@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = recipe_book.get_recipe(recipe_id)

    if request.method == "GET":
        return render_template("edit_recipe.html", recipe=recipe)

    if request.method == "POST":
        content = request.form["content"]
        title = request.form["title"]
        recipe_book.update_recipe(recipe["id"], title, content)
        return redirect("/recipe/" + str(recipe_id))
    
@app.route("/remove_recipe/<int:recipe_id>", methods=["GET"])
def remove_recipe(recipe_id):
    recipe = recipe_book.get_recipe(recipe_id)

    if request.method == "GET":
        return render_template("remove_recipe.html", recipe=recipe)

    if request.method == "POST":
        if "continue" in request.form:
            recipe_book.remove_recipe(recipe["id"])
        return redirect("/")
    


@app.route("/edit_rating/<int:rating_id>", methods=["GET", "POST"])
def edit_rating(rating_id):
    rating = recipe_book.get_rating(rating_id)
    print("stuff")
    if request.method == "GET":
        print(rating["id"])
        return render_template("edit_rating.html", rating=rating)

    if request.method == "POST":
        print("Editing rating...")
        content = request.form["content"]
        rating_num = request.form["dropdown"]
        recipe_book.update_rating(rating_id, content, rating_num)
        return redirect("/recipe/" + str(rating["recipe_id"]))
    
@app.route("/remove_rating/<int:rating_id>", methods=["GET", "POST"])
def remove_rating(rating_id):
    rating = recipe_book.get_rating(rating_id)

    if request.method == "GET":
        return render_template("remove_rating.html", rating=rating)

    if request.method == "POST":
        if "continue" in request.form:
            recipe_book.remove_rating(rating["id"])
        return redirect("/recipe/" + str(rating["recipe_id"]))


@app.route("/")
def index():
    recipes = recipe_book.get_recipes()
    return render_template("index.html", recipes=recipes)

