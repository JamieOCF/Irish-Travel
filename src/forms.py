from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SearchField, IntegerField, DecimalField, FloatField, PasswordField
from wtforms import RadioField, BooleanField, SubmitField, DateField, FileField
from wtforms.validators import InputRequired, NumberRange, EqualTo, DataRequired
from random import randint

class RegistrationForm(FlaskForm):
    user_id = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Repeat password:", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    user_id = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Submit")



class ChangeUserIDForm(FlaskForm):
    new_user_id = StringField("New Username:", validators=[InputRequired()])
    submit = SubmitField("Submit")

class ChangeUserPasswordForm(FlaskForm):
    new_password = PasswordField(" New Password:", validators=[InputRequired()])
    new_password2 = PasswordField("Repeat password:", validators=[InputRequired(), EqualTo("new_password")])
    submit = SubmitField("Submit")



class AddHotelForm(FlaskForm):
    located_in = SelectField("Located in:", validators=[InputRequired()])

    hotel_name = StringField("Hotel Name:", validators=[InputRequired()])
    rating = SelectField("Rating(1-5):", validators=[InputRequired()], choices=[1,2,3,4,5], default=3)
    price_2s = IntegerField("2 Singles:", validators=[InputRequired(), NumberRange(30,999)])
    price_3s = IntegerField("3 Singles:", validators=[InputRequired(), NumberRange(30,999)])
    price_1d = IntegerField("1 Double:", validators=[InputRequired(), NumberRange(30,999)])
    price_2d = IntegerField("2 Doubles:", validators=[InputRequired(), NumberRange(30,999)])
    price_1d1s = IntegerField("1 Double + 1 Single:", validators=[InputRequired(), NumberRange(30,999)])
    available_2s = SelectField("Available 2s Rooms:", validators=[InputRequired()], choices=[0,1,2,3,4,5,6,7], default=0)
    available_3s = SelectField("Available 3s Rooms:", validators=[InputRequired()], choices=[0,1,2,3,4,5,6,7], default=0)
    available_1d = SelectField("Available 1d Rooms:", validators=[InputRequired()], choices=[0,1,2,3,4,5,6,7], default=0)
    available_2d = SelectField("Available 2d Rooms:", validators=[InputRequired()], choices=[0,1,2,3,4,5,6,7], default=0)
    available_1d1s = SelectField("Available 1d1s Rooms:", validators=[InputRequired()], choices=[0,1,2,3,4,5,6,7], default=0)
    submit = SubmitField("Submit")

class AddDestinationForm(FlaskForm):
    city_name = StringField("City Name:", validators=[InputRequired()])
    country = StringField("Country Name:", validators=[InputRequired()])
    submit = SubmitField("Submit")

class AddRouteForm(FlaskForm):
    airline = SelectField("Airline:", validators=[InputRequired()])

    from_city = SelectField("Irish Airport:", validators=[InputRequired()], choices=["Dublin","Cork","Shannon"], default="Dublin")
    to_city = SelectField("Destination City:", validators=[InputRequired()])
    duration = IntegerField("Duration(Mins):", validators=[InputRequired()])
    price_eco = IntegerField("Economy Price:", validators=[InputRequired(), NumberRange(5,999)])
    price_bus = IntegerField("Business Price:", validators=[InputRequired(), NumberRange(5,999)])
    price_fc = IntegerField("First Class Price:", validators=[InputRequired(), NumberRange(5,999)])
    available_eco = SelectField("Economy Tickets:", validators=[InputRequired()], choices=[0,1,2,3,4,5,6,7,8,9,10], default=5)
    available_bus = SelectField("Business Tickets:", validators=[InputRequired()], choices=[0,1,2,3,4,5,6,7,8,9,10], default=5)
    available_fc = SelectField("First Class Tickets:", validators=[InputRequired()], choices=[0,1,2,3,4,5,6,7,8,9,10], default=5)
    submit = SubmitField("Submit")

class AddAirlineForm(FlaskForm):
    airline_name = StringField("Airline Name:", validators=[InputRequired()])
    airline_rating = SelectField("Airline Rating:", validators=[InputRequired()], choices=[1,2,3,4,5,6,7,8,9,10], default=10)
    submit = SubmitField("Submit")

class ConfirmRemoveForm(FlaskForm):
    confirm = SelectField("Are you sure?", validators=[InputRequired()], choices=["Yes", "No"], default="No")
    submit = SubmitField("Submit")

class ConfirmAirlineRemoveForm(FlaskForm):
    confirm = SelectField("Are you sure?", validators=[InputRequired()], choices=["Yes", "No"], default="No")
    transfer_to = SelectField("Transfer Routes to:", validators=[InputRequired()])
    submit = SubmitField("Submit")




class ChooseDateForm(FlaskForm):
    from_date = DateField("From:", validators=[InputRequired()])
    to_date = DateField("To:", validators=[InputRequired()])
    submit = SubmitField("Submit")


class ChooseDestinationForm(FlaskForm):
    destination = SelectField("Your Destination:", validators=[InputRequired()])
    submit = SubmitField("Submit")


class ChooseFlightRouteForm(FlaskForm):
    from_city = RadioField("From:", validators=[InputRequired()])
    to_city = StringField("To:")
    submit = SubmitField("Submit")

class ChooseAirlineForm(FlaskForm):
    airline = SelectField("Choose Airline", validators=[InputRequired()])
    submit = SubmitField("Submit")

class ChooseSeatsForm(FlaskForm):
    num_eco_tix = SelectField("Number of Economy Tickets:", validators=[InputRequired()], choices=[0,1,2,3,4,5], default=0)
    num_bus_tix = SelectField("Number of Business Tickets:", validators=[InputRequired()], choices=[0,1,2,3,4], default=0)
    num_fc_tix = SelectField("Number of First Class Tickets:", validators=[InputRequired()], choices=[0,1,2,3], default=0)
    submit = SubmitField("Submit")


class ChooseHotelForm(FlaskForm):
    hotel = RadioField("Choose Hotel:", validators=[InputRequired()])
        #display hotels + ratings in chosen location
    submit = SubmitField("Submit")

class ChooseRoomsForm(FlaskForm):
    num_2s = SelectField("2 Singles Rooms:", validators=[InputRequired()], choices=[0,1,2], default=0)
    num_3s = SelectField("3 Singles Rooms:", validators=[InputRequired()], choices=[0,1,2], default=0)
    num_1d = SelectField("1 Double Rooms:", validators=[InputRequired()], choices=[0,1,2], default=0)
    num_2d = SelectField("2 Doubles Rooms:", validators=[InputRequired()], choices=[0,1,2], default=0)
    num_1d1s = SelectField("Single + Double Rooms:", validators=[InputRequired()], choices=[0,1,2], default=0)
    submit = SubmitField("Submit")

class ConfirmBookingForm(FlaskForm):
    confirm = SelectField("Confirm Booking/ or Restart?", validators=[InputRequired()], choices=["Confirm", "Restart"], default="Confirm")
    submit = SubmitField("Submit")

class MakeAdminForm(FlaskForm):
    user = SelectField("Select User:", validators=[InputRequired()])
    submit = SubmitField("Submit")