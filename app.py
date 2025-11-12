import sqlite3
from flask import Flask
from flask import abort, make_response, redirect, render_template, request, session, flash
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
def new_thread():
    title = request.form["title"]
    content = request.form["content"]
    user_id = session["user_id"]

    thread_id = recipe_book.add_recipe(title, content, user_id)
    return redirect("/thread/" + str(thread_id))


@app.route("/")
def index():
    recipes = recipe_book.get_recipes()
    print(recipes)
    return render_template("index.html", recipes=recipes)

