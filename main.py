from flask import Flask, redirect, url_for, request, render_template, flash
from flask_bootstrap import Bootstrap5
import os
from dotenv import load_dotenv
import logging
from flask_wtf import CSRFProtect
from database import init_db, db_session



from models import User, Job
from forms import UserForm, JobForm
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

@app.route("/jobs", methods=["GET"])
def show_jobs():
    jobs = Job.query.all()
    return render_template("jobs.html", jobs=jobs)



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

@app.route("/user/<int:user_id>", methods=["GET", "POST"])
def show_user_form_update(user_id):
    message = ""
    user = User.query.filter(User.id == user_id).first()
    if not user:
        return render_template("404.html", title="404"), 404
    form = UserForm(obj=user)
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        birth_year = form.birth_year.data
        user.name = name
        user.surname = surname
        user.birth_year = birth_year
        db_session.commit()
        return redirect(url_for("show_users"))
    return render_template("user_form.html", form=form, message=message, user=user)



@app.route('/job/<uid>', methods=['GET','POST'])
def show_job_form(uid):
    message = ""
    user = User.query.filter(User.id == uid).first()
    form = JobForm(user=user)
    if form.validate_on_submit():
        name = form.name.data
        job = Job(name=name, user=user)
        db_session.add(job)
        db_session.commit()
        jobs = user.jobs
        flash('Record was successfully added')
        return render_template("user_jobs.html", user=user, jobs=jobs)
    return render_template("user_form.html", form=form, message=message, user=user)


@app.route("/job/<uid>/<jid>/delete", methods = ["GET"])
def delete_job(uid, jid):
    user = User.query.filter(User.id == uid).first()
    job = Job.query.filter(Job.id == jid).first()
    db_session.delete(job)
    user.jobs.remove(job)
    db_session.commit()
    jobs = user.jobs
    return render_template("user_jobs.html", user=user, jobs=jobs)


@app.route("/jobs/<user_id>", methods=["GET"])
def show_user_jobs(user_id):
    user = User.query.filter(User.id == user_id).first()
    jobs = user.jobs
    return render_template("user_jobs.html", user=user, jobs=jobs)


@app.route("/job/<jid>", methods=["DELETE"])
def delete_job_by_id(jid):
    job = Job.query.filter(Job.id == jid).first()
    user = job.user

    print(job)
    db_session.delete(job)
    db_session.commit()
    jobs = user.jobs
    return render_template("user_jobs.html", user=user, jobs=jobs)
