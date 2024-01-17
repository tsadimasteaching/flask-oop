from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, IntegerField, EmailField
from wtforms.validators import DataRequired, Length


class UserForm(FlaskForm):
    # id = IntegerField("Id?", validators=[DataRequired()])
    name = StringField("What is your name?", validators=[DataRequired(), Length(5, 40)])
    surname = StringField(
        "What is your surname?", validators=[DataRequired(), Length(5, 40)]
    )
    birth_year = IntegerField("Year of Birth?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class JobForm(FlaskForm):
    name = StringField("What is your job?", validators=[DataRequired(), Length(5, 40)])
    submit = SubmitField("Submit")