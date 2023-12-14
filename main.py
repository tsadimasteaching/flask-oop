from flask import Flask, redirect, url_for, request, render_template
import os
from dotenv import load_dotenv
import logging
from models import User

logging.basicConfig(filename="record.log", level=logging.DEBUG)


app = Flask(__name__)

app.logger.info("Environmental variable Initialized")

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print("APP_NAME is {}".format(os.environ.get("APP_NAME")))
else:
    raise RuntimeError("Not found application configuration")

users = []


@app.route("/")
def hello():
    return "Hello World!"


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
        print(user)
        return redirect(url_for("show_users", users=users))


@app.route("/users", methods=["GET"])
def show_users():
    return render_template("users.html", users=users)
