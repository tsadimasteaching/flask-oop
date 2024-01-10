from flask import Flask, redirect, url_for, request, render_template
from flask_bootstrap import Bootstrap5
import os
from dotenv import load_dotenv
import logging
from flask_wtf import CSRFProtect
import pickle


from models import User
from forms import UserForm
from utils import search_user_by_id, update_user_in_users
import os

logging.basicConfig(filename="record.log", level=logging.DEBUG)


app = Flask(__name__)
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

import secrets

foo = secrets.token_urlsafe(16)
app.secret_key = foo

app.logger.info("Environmental variable Initialized")

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    USERFILE = os.environ.get("USERFILE")
    print("APP_NAME is {}".format(os.environ.get("APP_NAME")))
    print("USER FILE is {}".format(USERFILE))
else:
    raise RuntimeError("Not found application configuration")

file_path = USERFILE
try:
    users_file = open(file_path, "rb")
except FileNotFoundError:
    users_file = open(file_path, "a")

if os.stat(file_path).st_size > 0:
    print("file > 0")
    users = pickle.load(users_file)
else:
    users = []
users_file.close()


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/hello/<string:username>")
def say_hello(username):
    return f"Hello {username}"


@app.route("/number/<int:num>")
def get_number(num):
    return f"Number {num}"


@app.route("/user", methods=["GET", "POST"])
def user_form():
    if request.method == "GET":
        return render_template("user_form.html")
    else:
        name = request.form["name"]
        surname = request.form["surname"]
        birth_year = request.form["birth_year"]
        user = User(name, surname, birth_year)
        users.append(user)
        users_file = open(file_path, "wb")
        pickle.dump(users, users_file)
        users_file.close()
        return redirect(url_for("show_users", users=users))


@app.route("/users", methods=["GET"])
def show_users():
    return render_template("users.html", users=users)


@app.route("/fuser", methods=["GET", "POST"])
def show_user_form():
    form = UserForm()
    message = ""
    if form.validate_on_submit():
        id = form.id.data
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        birth_year = form.birth_year.data
        user = User(id, name, surname, email, birth_year)
        users.append(user)
        users_file = open(file_path, "wb")
        pickle.dump(users, users_file)
        users_file.close()
        return redirect(url_for("show_users", users=users))
    return render_template("fuser_form.html", form=form, message=message)


@app.route("/user/<int:id>", methods=["GET", "POST"])
def edit_user(id):
    user = search_user_by_id(users, id)
    app.logger.info(user)
    if not user:
        return render_template("404.html", title="404"), 404
    form = UserForm(obj=user)
    message = ""
    if form.validate_on_submit():
        id = form.id.data
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        birth_year = form.birth_year.data
        upd_user = User(id, name, surname, email, birth_year)
        update_user_in_users(users, upd_user)
        return redirect(url_for("show_users", users=users))
    return render_template("fuser_form.html", form=form, message=message)
