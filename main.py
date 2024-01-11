from flask import Flask, redirect, url_for, request, render_template
from flask_bootstrap import Bootstrap5
import os
from dotenv import load_dotenv
import logging
from flask_wtf import CSRFProtect
from database import init_db, db_session



from models import User
from forms import UserForm
from utils import search_user_by_id, update_user_in_users
import os

logging.basicConfig(filename="record.log", level=logging.DEBUG)


app = Flask(__name__)
# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)


with app.app_context():
    init_db()



import secrets

foo = secrets.token_urlsafe(16)
app.secret_key = foo




@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.close()

@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/users", methods=["GET"])
def show_users():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/user", methods=["GET", "POST"])
def show_user_form():
    form = UserForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        birth_year = form.birth_year.data
        user = User(name=name, surname=surname, birth_year=birth_year)
        db_session.add(user)
        db_session.commit()
        return redirect(url_for("show_users"))
        #return redirect(url_for("show_users", users=users))
    return render_template("user_form.html", form=form, message=message)

