from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, IntegerField, EmailField
from wtforms.validators import DataRequired, Length


class UserForm(FlaskForm):
    id = IntegerField("Id?", validators=[DataRequired()])
    name = StringField("What is your name?", validators=[DataRequired(), Length(5, 40)])
    surname = StringField(
        "What is your surname?", validators=[DataRequired(), Length(5, 40)]
    )
    email = EmailField("Which is your email?")
    birth_year = IntegerField("Year of Birth?", validators=[DataRequired()])
    submit = SubmitField("Submit")
