from flask import Flask, redirect, url_for, request, render_template
from flask_bootstrap import Bootstrap5
import os
from dotenv import load_dotenv
import logging
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


from models import User

logging.basicConfig(filename="record.log", level=logging.DEBUG)


app = Flask(__name__)
# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

import secrets

foo = secrets.token_urlsafe(16)
app.secret_key = foo

app.logger.info("Environmental variable Initialized")

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print("APP_NAME is {}".format(os.environ.get("APP_NAME")))
else:
    raise RuntimeError("Not found application configuration")

users = []


class UserForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired(), Length(5, 40)])
    surname = StringField(
        "What is your surname?", validators=[DataRequired(), Length(5, 40)]
    )
    birth_year = IntegerField("Year of Birth?", validators=[DataRequired()])
    submit = SubmitField("Submit")


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
        print(user)
        return redirect(url_for("show_users", users=users))


@app.route("/users", methods=["GET"])
def show_users():
    return render_template("users.html", users=users)


@app.route("/fuser", methods=["GET", "POST"])
def show_user_form():
    form = UserForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        birth_year = form.birth_year.data
        user = User(name, surname, birth_year)
        users.append(user)
        print(user)
        return redirect(url_for("show_users", users=users))
    return render_template("fuser_form.html", form=form, message=message)
