import sqlite3
import math
import time
import secrets
from flask import g
from flask import Flask
from flask import redirect, abort, render_template, request, session, flash, make_response
import config, users, recipe_book

app = Flask(__name__)
app.secret_key = config.secret_key


def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf(request):
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        filled = {"username": username}
        if password1 != password2:
            flash("Error: The passwords are not the same")
            return render_template("register.html", filled=filled)
        if password1 == "" and password2 == "":
            flash("Error: Password field can't be empty")
            return render_template("register.html", filled=filled)
        if username == "":
            flash("Error: username field can't be empty")
            return render_template("register.html", filled=filled)
        try:
            users.create_user(username, password1)
            flash("Registration was succesful, you can now log in")
            return redirect("/login")            
        except sqlite3.IntegrityError:
            flash("Error: username is already taken")
            return render_template("register.html", filled=filled)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", next_page=request.referrer, filled={})

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_id = users.check_login(username, password)
        next_page = request.form["next_page"]
        if user_id:
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
            session["username"] = username
            flash("login successful!")
            return redirect(next_page)
        else:
            filled = {"username": username}
            flash("Error: Incorrect username or password")
            return render_template("login.html", next_page=request.referrer, filled=filled)
@app.route("/logout")
def logout():
    del session["user_id"]
    del session["csrf_token"]
    del session["username"]
    return redirect("/")

@app.route("/new_recipe", methods=["POST"])
def new_recipe():
    require_login()
    title = request.form["title"]
    content = request.form["content"]
    user_id = session["user_id"]


    if not title or not content or len(title) > 100 or len(content) > 5000:
        abort(403)
    try:
        recipe_id = recipe_book.add_recipe(title, content, user_id)
    except sqlite3.IntegrityError:
        abort(403)
    all_classes = recipe_book.get_all_classes()
    classes = []
    for elem in all_classes:
        try:
            classes.append(request.form[elem["title"]])
        except KeyError:
            continue

    for title in classes:
        recipe_book.add_recipe_class(recipe_id, title)

    return redirect("/recipe/" + str(recipe_id))

@app.route("/new_rating", methods=["POST"])
def new_rating():
    require_login()
    content = request.form["content"]
    user_id = session["user_id"]
    recipe_id = request.form["recipe_id"]
    rating = request.form["dropdown"]

    if not content or len(content) > 5000:
        abort(403)
    try:
        recipe_book.add_rating(content, rating,  user_id, recipe_id)
    except sqlite3.IntegrityError:
        abort(403)
    return redirect("/recipe/" + str(recipe_id))

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = recipe_book.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    ratings = recipe_book.get_ratings(recipe_id)
    classes = recipe_book.get_classes_of_recipe(recipe_id)
    return render_template("recipe.html", recipe=recipe, ratings=ratings, classes=classes)


@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    require_login()
    recipe = recipe_book.get_recipe(recipe_id)
    all_classes = recipe_book.get_all_classes()
    if recipe["user_id"] != session["user_id"]:
        abort(403)
        
    if request.method == "GET":
        return render_template("edit_recipe.html", recipe=recipe, classes=all_classes)

    if request.method == "POST":
        content = request.form["content"]
        title = request.form["title"]
        if not title or not content or len(title) > 100 or len(content) > 5000:
            abort(403)
        recipe_book.update_recipe(recipe["id"], title, content)
        classes = []
        for elem in all_classes:
            try:
                classes.append(request.form[elem["title"]])
            except KeyError:
                continue

        for title in classes:
            recipe_book.add_recipe_class(recipe_id, title)
        return redirect("/recipe/" + str(recipe_id))
    
@app.route("/remove_recipe/<int:recipe_id>", methods=["GET", "POST"])
def remove_recipe(recipe_id):
    require_login()
    recipe = recipe_book.get_recipe(recipe_id)
    if recipe["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("remove_recipe.html", recipe=recipe)

    if request.method == "POST":
        if "continue" in request.form:
            recipe_book.remove_recipe(recipe["id"])
        return redirect("/")
    


@app.route("/edit_rating/<int:rating_id>", methods=["GET", "POST"])
def edit_rating(rating_id):
    require_login()
    rating = recipe_book.get_rating(rating_id)
    if rating["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("edit_rating.html", rating=rating)

    if request.method == "POST":
        content = request.form["content"]
        rating_num = request.form["dropdown"]
        if not content or len(content) > 5000:
            abort(403)
        recipe_book.update_rating(rating_id, content, rating_num)
        return redirect("/recipe/" + str(rating["recipe_id"]))
    
@app.route("/remove_rating/<int:rating_id>", methods=["GET", "POST"])
def remove_rating(rating_id):
    require_login()
    rating = recipe_book.get_rating(rating_id)
    if rating["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("remove_rating.html", rating=rating)

    if request.method == "POST":
        if "continue" in request.form:
            recipe_book.remove_rating(rating["id"])
        return redirect("/recipe/" + str(rating["recipe_id"]))


@app.route("/search")
def search():
    all_classes = recipe_book.get_all_classes()
    query = request.args.get("query")
    classes = []
    tags = request.full_path.split("&")[1:]
    for tag in tags:
        checked_class = tag.split("=")[0]
        classes.append(checked_class)
    classes = [elem for elem in classes if elem]
    results = recipe_book.search(query, classes) if (query or classes) else []
    return render_template("search.html", query=query, results=results, all_classes=all_classes, classes=classes)



@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    recipes = recipe_book.get_recipes_by_user(user_id)
    return render_template("user.html", user=user, recipes=recipes)

@app.route("/add_image", methods=["GET", "POST"])
def add_image():
    require_login()
    if request.method == "GET":
        return render_template("add_image.html")

    if request.method == "POST":
        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            return "VIRHE: väärä tiedostomuoto"

        image = file.read()
        if len(image) > 100 * 1024:
            return "VIRHE: liian suuri kuva"

        user_id = session["user_id"]
        users.update_image(user_id, image)
        flash("The upload was succesful!")
        return redirect("/user/" + str(user_id))

@app.route("/image/<int:user_id>")
def show_image(user_id):
    image = users.get_image(user_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response



@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    thread_count =  recipe_book.get_recipe_count()
    recipes = recipe_book.get_recipes(page, page_size)
    classes = recipe_book.get_all_classes()
    page_count = math.ceil(thread_count / page_size)
    page_count = max(page_count, 1)
    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))
    return render_template("index.html", recipes=recipes, classes=classes, page=page, page_count=page_count)


@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response