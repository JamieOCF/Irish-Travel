from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SearchField, IntegerField, DecimalField, FloatField, PasswordField
from wtforms import RadioField, BooleanField, SubmitField, DateField, FileField
from wtforms.validators import InputRequired, NumberRange, EqualTo, DataRequired
from random import randint

#########################
#AUTH
#########################
class RegistrationForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Repeat password:", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Submit")



#########################
#ADMIN
#########################
class CompaniesForm(FlaskForm):
    company_name = StringField("Company Name:", validators=[InputRequired()])
    transport_mode = SelectField("Transport Mode:", validators=[InputRequired()], choices=["Flights", "Ferries", "Buses", "Trains"], default="Flights")
    submit = SubmitField("Confirm")

class DestinationsForm(FlaskForm):
    city_name = StringField("City Name:", validators=[InputRequired()])
    country = StringField("Country Name:", validators=[InputRequired()])
    submit = SubmitField("Confirm")