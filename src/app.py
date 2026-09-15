from flask import Flask, render_template, session, redirect, url_for, g
from database import get_db, close_db 
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

from forms import RegistrationForm, LoginForm, ChangeUserIDForm, ChangeUserPasswordForm
from forms import AddHotelForm, AddAirlineForm, AddDestinationForm, AddRouteForm, ConfirmRemoveForm, ConfirmAirlineRemoveForm
from forms import ChooseDateForm, ChooseDestinationForm, ChooseFlightRouteForm, ChooseAirlineForm, ChooseSeatsForm, ChooseHotelForm, ChooseRoomsForm, ConfirmBookingForm
from forms import MakeAdminForm

from datetime import datetime, timedelta
from functools import wraps
import string


app = Flask(__name__)
app.config.from_pyfile("config.py")
Session(app)
app.teardown_appcontext(close_db)


@app.before_request
def load_logged_in_user():
    g.user_id = session.get("user_id", None)
    session["is_admin"] = 0
    session.modified = True

    if g.user_id is not None:
        db = get_db()
        user = db.execute("""SELECT * FROM users WHERE user_id = ?;""", (g.user_id,)).fetchone()
        if user is not None:
            if user["is_admin"] == 1:       #Keep " g.user_id == "admin" "? --> Will have to change other functionalities if changed (e.g. navbar)
                session["is_admin"] = 1
                session.modified = True
                g.is_admin = True

            elif user["is_admin"] == 2:
                session["is_admin"] = 2
                session.modified = True
                g.is_main_admin = True

'''
#On navbar:
    #If is_main_admin account: Admin tab displayed
    #If user account made admin: Admin tab and User tab displayed
    #If non-admin user account: User tab displayed
'''


#wrappers
def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user_id == None:
            return redirect(url_for("home_page"))
        elif session["is_admin"] == 0:
            return redirect(url_for("user"))
        return view(*args, **kwargs)
    return wrapped_view

def not_main_admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user_id == None:
            return redirect(url_for("login"))
        elif session["user_id"] == "admin":
            return redirect(url_for("admin"))
        return view(*args, **kwargs)
    return wrapped_view

def initialise_booking(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        session["booking"] = {}
        session.modified = True


        session["booking"]["from_date"] = None
        session.modified = True

        session["booking"]["to_date"] = None
        session.modified = True

        session["booking"]["holiday_length"] = None


        session["booking"]["destination"] = None
        session.modified = True


        session["booking"]["flight"] = {}
        session.modified = True

        session["booking"]["flight"]["route_id"] = None
        session.modified = True

        session["booking"]["flight"]["from_city"] = None
        session.modified = True

        session["booking"]["flight"]["to_city"] = None
        session.modified = True

        session["booking"]["flight"]["airline"] = None
        session.modified = True

        session["booking"]["flight"]["tickets"] = {}
        session.modified = True
        session["booking"]["flight"]["tickets"]["num_eco_tix"] = None
        session.modified = True
        session["booking"]["flight"]["tickets"]["num_bus_tix"] = None
        session.modified = True
        session["booking"]["flight"]["tickets"]["num_fc_tix"] = None
        session.modified = True

        session["booking"]["flight"]["cost"] = 0


        session["booking"]["hotel"] = {}
        session.modified = True

        session["booking"]["hotel_id"] = None
        session.modified = True

        session["booking"]["hotel"]["hotel_name"] = None
        session.modified = True

        session["booking"]["hotel"]["rooms"] = {}
        session.modified = True
        session["booking"]["hotel"]["rooms"]["num_2s_rooms"] = None
        session.modified = True
        session["booking"]["hotel"]["rooms"]["num_3s_rooms"] = None
        session.modified = True
        session["booking"]["hotel"]["rooms"]["num_1d_rooms"] = None
        session.modified = True
        session["booking"]["hotel"]["rooms"]["num_2d_rooms"] = None
        session.modified = True
        session["booking"]["hotel"]["rooms"]["num_1d1s_rooms"] = None
        session.modified = True

        session["booking"]["hotel"]["cost"] = 0


        session["booking"]["cost"] = 0
        session.modified = True
        return view(*args, **kwargs)
    return wrapped_view


#booking check if skip steps
def check_dates():
    if session["booking"]["from_date"] == None or session["booking"]["to_date"] == None or session["booking"]["holiday_length"] == None:
        print("test")
        return redirect(url_for('choose_dates'))
    
def check_destination():
    if session["booking"]["destination"] == None:
        return redirect(url_for('choose_destination'))
    else:
        check_dates()

def check_flight_route():
    if session["booking"]["flight"]["from_city"] == None or session["booking"]["flight"]["to_city"] == None:
        return redirect(url_for('choose_flight'))
    else:
        check_destination()

def check_airline():
    if session["booking"]["flight"]["airline"] == None:
        return redirect(url_for('choose_airline'))
    else:
        check_flight_route()

def check_seats():
    if session["booking"]["flight"]["tickets"] == {}:
        return redirect(url_for('choose_tickets'))
    else:
        check_airline()

def check_hotel():
    if session["booking"]["hotel"]["hotel_name"] == None:
        return redirect(url_for('choose_hotel'))
    else:
        check_seats()

def check_rooms():
    if session["booking"]["hotel"]["rooms"] == {}:
        return redirect(url_for('choose_rooms'))
    else:
        check_hotel()




#base routes
@app.route("/")
@initialise_booking
def home_page():
    session["url"] = url_for("home_page")
    session.modified = True
    return render_template("ux/home_page.html", style="styles.css")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        clash = db.execute("""SELECT * FROM users WHERE user_id = ?;""",
                           (user_id,)).fetchone()
        if clash is not None:
            form.user_id.errors.append("Username already taken!")
        else:
            db.execute("""INSERT INTO users (user_id, password, is_admin)
                       VALUES (?, ?, ?);""", (user_id, generate_password_hash(password), 0))
            db.commit()
            return redirect(url_for("login"))
    return render_template("auth/register.html", style="register.css", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        user_in_db = db.execute("""SELECT * FROM users WHERE user_id = ?;""",
                   (user_id,)).fetchone()
        if user_in_db is None:
            form.user_id.errors.append("Username doesn't exist!")
        elif not check_password_hash(user_in_db["password"], password):
            form.password.errors.append("Wrong Password!")
        else:
            session["user_id"] = user_id
            session.modified = True

            next_page = session["url"]
            if not next_page:
                next_page = url_for("home_page")

            if user_in_db["is_admin"] == 2:
                g.is_main_admin = True


            return redirect(next_page)
    return render_template("auth/login.html", style="login.css", form=form)

@app.route("/logout")
def logout():
    session.clear()
    session.modified = True
    return redirect(url_for("home_page"))



#user routes
@app.route("/user", methods=["GET", "POST"])
@not_main_admin_required
def user():
    db = get_db()
    all_bookings = db.execute("""SELECT * FROM flight_bookings AS fb JOIN hotel_bookings AS hb JOIN routes AS r JOIN hotels AS h
                                    ON fb.user_id = hb.user_id 
                                    AND fb.flight_booking_num = hb.hotel_booking_num
                                    AND fb.route_id = r.route_id
                                    AND hb.hotel_id = h.hotel_id
                              WHERE fb.user_id = ? ORDER BY fb.flight_booking_num;""", (g.user_id,)).fetchall()
    print(all_bookings)

    return render_template("user/user.html", all_bookings=all_bookings, style="user.css")

@app.route("/change_username", methods=["GET", "POST"])
@not_main_admin_required
def change_username():
    form = ChangeUserIDForm()
    db = get_db()
    message = "_____"

    if form.validate_on_submit():
        new_user_id = form.new_user_id.data
        user_data = db.execute("""SELECT * FROM users WHERE user_id = ?;""", (new_user_id,)).fetchone()

        if new_user_id == g.user_id:
            form.new_user_id.errors.append("New username must be different!")
        elif user_data is not None:
            form.new_user_id.errors.append("That username is taken!")
        else:
            db.execute("""UPDATE users SET user_id = ? WHERE user_id = ?;""", (new_user_id, g.user_id))
            db.commit()
            session["user_id"] = new_user_id
            session.modified = True
            message = "Username updated successfully!"
    return render_template("user/change_username.html", form=form, message=message)

@app.route("/change_password", methods=["GET", "POST"])
@not_main_admin_required
def change_password():
    form = ChangeUserPasswordForm()
    db = get_db()
    message = "_____"

    if form.validate_on_submit():
        new_password = form.new_password.data

        password = db.execute("""SELECT * FROM USERS WHERE user_id = ?;""", (g.user_id,)).fetchone()
        password = password["password"]

        if check_password_hash(password, new_password):
            form.new_password.errors.append("New password must be different to old password!")
        else:
            db.execute("""UPDATE users SET password = ? WHERE user_id = ?;""", 
                       (generate_password_hash(new_password), g.user_id))
            db.commit()
            message = "Password updated successfully!"
    return render_template("user/change_password.html", form=form, message=message)


#showcases
@app.route("/destinations")
def destinations():
    session["url"] = url_for("destinations")
    session.modified = True
    db = get_db()
    destinations = db.execute("""SELECT * FROM destinations""")
    return render_template("ux/destinations.html", destinations=destinations)

@app.route("/hotels")
def hotels():
    session["url"] = url_for("hotels")
    session.modified = True
    db = get_db()
    hotels = db.execute("""SELECT * FROM hotels""")
    return render_template("ux/hotels.html", hotels=hotels)


@app.route("/wishlist")
@not_main_admin_required
def wishlist():
    session["url"] = url_for("wishlist")
    session.modified = True
    if g.user_id is None:
        return redirect(url_for("login"))

    return render_template("wishlist.html")


#admin stuff
@app.route("/set_admin")
@admin_required
def set_admin():
    return

@app.route("/revoke_admin")
@admin_required
def revoke_admin():
    #if g.user == "admin": skip
    return

@app.route("/admin")
@admin_required
def admin():
    return render_template("admin_page.html", style="admin.css")




@app.route("/add_hotel", methods=["GET", "POST"])
@admin_required
def add_hotel():
    form = AddHotelForm()
    message = "_____"
    db = get_db()

    form.located_in.choices = [city["city_name"] for city in db.execute("""SELECT * FROM destinations;""").fetchall()]

    if form.validate_on_submit():
        located_in = form.located_in.data

        hotel_name = form.hotel_name.data
        rating = form.rating.data
        price_2s = form.price_2s.data
        price_3s = form.price_3s.data
        price_1d = form.price_1d.data
        price_2d = form.price_2d.data
        price_1d1s = form.price_1d1s.data
        available_2s = form.available_2s.data
        available_3s = form.available_3s.data
        available_1d = form.available_1d.data
        available_2d = form.available_2d.data
        available_1d1s = form.available_1d1s.data

        clash = db.execute("""SELECT * FROM hotels WHERE hotel_name = ?;""", (hotel_name,)).fetchone()

        if clash is not None:
            form.hotel_name.errors.append("That hotel name already exists!")
        else:
            db.execute("""INSERT INTO hotels(hotel_name, rating, price_2s, price_3s, price_1d, price_2d, price_1d1s, 
                    available_2s, available_3s, available_1d, available_2d, available_1d1s)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?);""", 
                    (hotel_name, rating, price_2s, price_3s, price_1d, price_2d, price_1d1s,
                        available_2s, available_3s, available_1d, available_2d, available_1d1s))
            db.commit()

            location = db.execute("""SELECT * FROM destinations WHERE city_name = ?;""", (located_in,)).fetchone()
            location_id = location["city_id"]
            hotel = db.execute("""SELECT * FROM hotels WHERE hotel_name = ?;""", (hotel_name,)).fetchone()
            hotel_id = hotel["hotel_id"]

            db.execute("""INSERT INTO is_located_in (hotel_id, city_id) VALUES (?,?);""", (hotel_id, location_id))
            db.commit()
            message = "Insertion Successful!"
    return render_template("add_hotel.html", form=form, message=message)

@app.route("/hotel_directory")
@admin_required
def hotel_directory():
    db = get_db()
    hotels = db.execute("""SELECT *
                        FROM hotels AS h JOIN is_located_in AS ili JOIN destinations AS d
                            ON h.hotel_id = ili.hotel_id AND ili.city_id = d.city_id
                        ORDER BY ili.city_id;""")
    return render_template("hotel_directory.html", hotels=hotels, style="hotel_directory.css")

@app.route("/remove_hotel/<int:hotel_id>", methods=["GET", "POST"])
@admin_required
def remove_hotel(hotel_id):
    form = ConfirmRemoveForm()
    db = get_db()
    message = ""

    id = db.execute("""SELECT * FROM hotels WHERE hotel_id = ?;""", (hotel_id,)).fetchone()

    if id is not None:
        city = db.execute("""SELECT * FROM hotels AS h JOIN is_located_in AS isi JOIN destinations AS d
                        ON h.hotel_id = isi.hotel_id AND isi.city_id = d.city_id
                    WHERE d.city_name = (SELECT d.city_name FROM hotels AS h JOIN is_located_in AS isi JOIN destinations AS d
                                        ON h.hotel_id = isi.hotel_id AND isi.city_id = d.city_id
                                    WHERE h.hotel_id = ?);""", (hotel_id,)).fetchall()
        city2 = city[0]["city_name"]
        if len(city) < 2:
            message = f"WARNING, there is only one hotel in {city2}! Removing this may cause this destination to have no hotels!"

        if form.validate_on_submit():
            confirm = form.confirm.data
            if confirm == "Yes":
                db.execute("""DELETE FROM hotels WHERE hotel_id = ?;""", (hotel_id,))
                db.commit()
                db.execute("""DELETE FROM is_located_in WHERE hotel_id = ?;""", (hotel_id,))
                db.commit()
            return redirect(url_for('hotel_directory'))
    else:
        return redirect(url_for('hotel_directory'))
    
    return render_template("remove_hotel.html", form=form, message=message, style="remove.css")




@app.route("/add_route", methods=["GET", "POST"])
@admin_required
def add_route():
    form = AddRouteForm()
    message = "_____"
    db = get_db()

    form.to_city.choices = [city["city_name"] for city in db.execute("""SELECT * FROM destinations;""").fetchall()]
    form.airline.choices = [airline["airline_name"] for airline in db.execute("""SELECT * FROM airlines;""").fetchall()]

    if form.validate_on_submit():
        airline = form.airline.data

        from_city = form.from_city.data
        to_city = form.to_city.data
        duration = form.duration.data
        price_eco = form.price_eco.data
        price_bus = form.price_bus.data
        price_fc = form.price_fc.data
        available_eco = form.available_eco.data
        available_bus = form.available_bus.data
        available_fc = form.available_fc.data

        clash = db.execute("""SELECT * FROM routes WHERE from_city = ? AND to_city = ? AND airline_name = ?;""", 
                            (from_city, to_city, airline)).fetchone()
        if clash is not None:
            form.airline.errors.append("This airline already operates this route!")
        else:
            db.execute("""INSERT INTO routes (from_city, to_city, duration, airline_name, price_eco, price_bus, price_fc,
                       available_eco, available_bus, available_fc)
                       VALUES (?,?,?,?,?,?,?,?,?,?);""", (from_city, to_city, duration, airline, price_eco, 
                        price_bus, price_fc, available_eco, available_bus, available_fc))
            db.commit()

            route = db.execute("""SELECT * FROM routes WHERE from_city = ? AND to_city = ? AND airline_name = ?;""", 
                            (from_city, to_city, airline)).fetchone()
            route_id = route["route_id"]

            airline = db.execute("""SELECT * FROM airlines WHERE airline_name = ?;""", (airline,)).fetchone()
            airline_id = airline["airline_id"]
            
            city = db.execute("""SELECT * FROM destinations WHERE city_name = ?;""", (to_city,)).fetchone()
            city_id = city["city_id"]
            

            db.execute("""INSERT INTO goes_to_and_from (route_id, city_id) VALUES (?,?);""", (route_id, city_id))
            db.commit()
            db.execute("""INSERT INTO flies_to_and_from (airline_id, city_id) VALUES (?,?);""", (airline_id, city_id))
            db.commit()
            db.execute("""INSERT INTO operates (airline_id, route_id) VALUES (?,?);""", (airline_id, route_id))
            db.commit()
            message = "Insertion Successful!"

    return render_template("add_route.html", form=form, message=message)

@app.route("/route_directory")
@admin_required
def route_directory():
    db = get_db()
    routes = db.execute("""SELECT * FROM routes ORDER BY from_city;""").fetchall()
    return render_template("route_directory.html", routes=routes, style="hotel_directory.css")

@app.route("/remove_route/<int:route_id>", methods=["GET", "POST"])
@admin_required
def remove_route(route_id):
    form = ConfirmRemoveForm()
    db = get_db()
    message = ""

    id = db.execute("""SELECT * FROM routes WHERE route_id = ?;""", (route_id,)).fetchone()

    if id is not None:
        to_city = db.execute("""SELECT * FROM routes WHERE to_city = (SELECT to_city FROM routes WHERE route_id = ?);""", (route_id,)).fetchall()

        city = to_city[0]["to_city"]
        if len(to_city) == 1:
            message = f"WARNING, there is only one flight that goes to {city}! Removing this route may cause a destination to become unreachable."

        if form.validate_on_submit():
            confirm = form.confirm.data
            if confirm == "Yes":
                gtaf = db.execute("""SELECT * FROM goes_to_and_from WHERE route_id = ?;""", (route_id,)).fetchone()
                city_id = gtaf["city_id"]
                op = db.execute("""SELECT * FROM operates WHERE route_id = ?;""", (route_id,)).fetchone()
                airline_id = op["airline_id"]

                db.execute("""DELETE FROM routes WHERE route_id = ?;""", (route_id,))
                db.commit()
                db.execute("""DELETE FROM goes_to_and_from WHERE route_id = ?;""", (route_id,))
                db.commit()
                db.execute("""DELETE FROM operates WHERE route_id = ?;""", (route_id,))
                db.commit()
                db.execute("""DELETE FROM flies_to_and_from WHERE city_id = ? AND airline_id = ?;""", (city_id, airline_id))
                db.commit()
            return redirect(url_for('route_directory'))
    else:
        return redirect(url_for('route_directory'))
    
    return render_template("remove_route.html", form=form, message=message, style="remove.css")



@app.route("/add_destination", methods=["GET", "POST"])
@admin_required
def add_destination():
    form = AddDestinationForm()
    db = get_db()
    message = "_____"

    if form.validate_on_submit():
        city_name = form.city_name.data
        city_name = city_name.capitalize()
        country = form.country.data
        country = country.capitalize()

        clash = db.execute("""SELECT * FROM destinations WHERE city_name = ? AND country = ?;""", (city_name, country)).fetchone()
        if clash is not None:
            form.city_name.errors.append(f"The destination {city_name}, in {country}, already  exists!")
        
        else:
            db.execute("""INSERT INTO destinations (city_name, country, image_link)
                    VALUES (?,?,?);""", (city_name, country, ""))
            db.commit()
            message = "Insertion Successful!"
    return render_template("add_destination.html", form=form, message=message)

@app.route("/destination_directory")
@admin_required
def destination_directory():
    db = get_db()
    destinations = db.execute("""SELECT * FROM destinations ORDER BY country;""").fetchall()
    return render_template("destination_directory.html", destinations=destinations, style="hotel_directory.css")

@app.route("/remove_destination/<int:city_id>", methods=["GET", "POST"])
@admin_required
def remove_destination(city_id):
    form = ConfirmRemoveForm()
    db = get_db()
    message = ""
    message2 = ""

    id = db.execute("""SELECT * FROM destinations WHERE city_id = ?;""", (city_id,)).fetchone()

    if id is not None:
        routes_to_city = db.execute("""SELECT * FROM routes WHERE to_city = (SELECT city_name FROM destinations WHERE city_id = ?);""", 
                                    (city_id,)).fetchall()
        hotels_in_city = db.execute("""SELECT * FROM hotels AS h JOIN is_located_in AS isi JOIN destinations AS d
                                            ON h.hotel_id = isi.hotel_id AND isi.city_id = d.city_id
                                    WHERE d.city_id = ?;""", (city_id,))
        routes_to_city = [x for x in routes_to_city]
        hotels_in_city = [y for y in hotels_in_city]

        if routes_to_city != []:
            city = routes_to_city[0]["to_city"]
            len_r = len(routes_to_city)
            if len_r > 1:
                message = f"Warning! There are {len_r} routes going to {city}. Continuing will remove them!"
            elif len_r == 1:
                message = f"Warning! There is {len_r} route going to {city}. Continuing will remove it!"
        if hotels_in_city != []:
            len_h = len(hotels_in_city)
            if len_h > 1:
                message2 = f"Warning! There are {len_h} hotels located in {city}. Continuing will remove them!"
            elif len_h == 1:
                message2 = f"Warning! There is {len_h} hotel located in {city}. Continuing will remove it!"
        

        if form.validate_on_submit():
            confirm = form.confirm.data
            if confirm == "Yes":
                for route in routes_to_city:
                    db.execute("""DELETE FROM routes WHERE route_id = ?;""", (route["route_id"],))
                    db.commit()
                    db.execute("""DELETE FROM goes_to_and_from WHERE route_id = ?;""", (route["route_id"],))
                    db.commit()
                    db.execute("""DELETE FROM operates WHERE route_id = ?;""", (route["route_id"],))
                    db.commit()
                db.execute("""DELETE FROM flies_to_and_from WHERE city_id = ?;""", (city_id,))
                db.commit()
                for hotel in hotels_in_city:
                    db.execute("""DELETE FROM hotels WHERE hotel_id = ?;""", (hotel["hotel_id"],))
                    db.commit()
                    db.execute("""DELETE FROM is_located_in WHERE hotel_id = ?;""", (hotel["hotel_id"],))
                    db.commit()
                db.execute("""DELETE FROM destinations WHERE city_id = ?;""", (city_id,))
                db.commit()
            return redirect(url_for('destination_directory'))
    else:
        return redirect(url_for('destination_directory'))

    return render_template("remove_destination.html", form=form, message=message, message2=message2, style="remove.css")


@app.route("/add_airline", methods=["GET", "POST"])
@admin_required
def add_airline():
    form = AddAirlineForm()
    db = get_db()
    message = "_____"

    if form.validate_on_submit():
        airline_name = form.airline_name.data
        airline_name = string.capwords(str(airline_name))
        print(airline_name)
        airline_rating = form.airline_rating.data

        clash = db.execute("""SELECT * FROM airlines WHERE airline_name = ?;""", (airline_name,)).fetchone()
        if clash is not None:
            form.airline_name.errors.append("This airline already exists!")
        elif airline_name == "None":
            form.airline_name.errors.append("Airline cannot be named 'None'!")

        else:
            db.execute("""INSERT INTO airlines (airline_name, airline_rating)
                       VALUES (?,?);""", (airline_name, airline_rating))
            db.commit()
            message = "Insertion Successful"
    return render_template("add_airline.html", form=form, message=message)

@app.route("/airline_directory")
@admin_required
def airline_directory():
    db = get_db()
    airlines = db.execute("""SELECT * FROM airlines ORDER BY airline_rating DESC;""").fetchall()
    return render_template("airline_directory.html", airlines=airlines, style="hotel_directory.css")

@app.route("/remove_airline/<int:airline_id>", methods=["GET", "POST"])
@admin_required
def remove_airline(airline_id):
    form = ConfirmAirlineRemoveForm()
    db = get_db()
    message = ""

    id = db.execute("""SELECT * FROM airlines WHERE airline_id = ?;""", (airline_id,)).fetchone()

    if id is not None:
        airline_list = [airline["airline_name"] for airline in db.execute("""SELECT * FROM airlines WHERE airline_id != ?;""", (airline_id,))]
        airline_list.insert(0,"None")
        form.transfer_to.choices = airline_list

        num_routes = db.execute("""SELECT COUNT(*) FROM operates WHERE airline_id = ? GROUP BY airline_id;""", (airline_id,)).fetchone()
        if num_routes is not None:
            num_routes = num_routes["COUNT(*)"]
            name = db.execute("""SELECT * FROM airlines WHERE airline_id = ?;""", (airline_id,)).fetchone()
            name = name["airline_name"]

            if num_routes > 1:
                message = f"NOTICE! {name} operates {num_routes} routes. You can transfer them to another airline or delete the routes"
            else:
                message = f"NOTICE! {name} operates {num_routes} route. You can transfer it to another airline or delete the route"


        if form.validate_on_submit():
            confirm = form.confirm.data
            transfer_to = form.transfer_to.data

            if confirm == "No":
                return redirect(url_for('airline_directory'))
            else:
                if transfer_to == "None": #delete routes/relationships
                    db.execute("""DELETE FROM goes_to_and_from 
                                WHERE route_id = (SELECT route_id FROM routes 
                                                    WHERE airline = (SELECT airline_name FROM airlines WHERE airline_id = ?));""", (airline_id,))
                    db.commit()

                    db.execute("""DELETE FROM routes WHERE airline = (SELECT airline_name FROM airlines WHERE airline_id = ?);""", (airline_id,))
                    db.commit()

                    db.execute("""DELETE FROM flies_to_and_from WHERE airline_id = ?;""", (airline_id,))
                    db.commit()
                else: #transfers routes/relationships
                    new_airline_id = db.execute("""SELECT * FROM airlines WHERE airline_name = ?;""", (transfer_to,)).fetchone()
                    new_airline_id = new_airline_id["airline_id"]
                    old_name = db.execute("""SELECT * FROM airlines WHERE airline_id = ?;""", (airline_id,)).fetchone()
                    old_name =old_name["airline_name"]

                    db.execute("""UPDATE operates SET airline_id = ? WHERE airline_id = ?;""", (new_airline_id, airline_id))
                    db.commit()
                    db.execute("""UPDATE routes SET airline_name = ? WHERE airline_name = ?;""", (transfer_to, old_name))
                    db.commit()
                    db.execute("""UPDATE flies_to_and_from SET airline_id = ? WHERE airline_id = ?;""", (new_airline_id, airline_id))
                    db.commit()
                
                #remove airline from db
                db.execute("""DELETE FROM airlines WHERE airline_id = ?;""", (airline_id,))
                db.commit()
            return redirect(url_for('airline_directory'))
    else:
        return redirect(url_for('airline_directory'))
    return render_template("remove_airline.html", form=form, message=message, style="remove.css")




#bookings
@app.route("/choose_dates", methods=["GET", "POST"])
@not_main_admin_required
@initialise_booking
def choose_dates():
    form = ChooseDateForm()

    if form.validate_on_submit():
        from_date = form.from_date.data
        to_date = form.to_date.data
    
        holiday_length = str(to_date - from_date)
        holiday_length = int(holiday_length[:1])

        session["booking"]["holiday_length"] = holiday_length
        session.modified = True

        today = datetime.date(datetime.now())
        max_date = today + timedelta(days=550)
        max_stay = from_date + timedelta(days=20)

        if from_date <= today:
            form.from_date.errors.append("Dates must be in the future!")
        elif to_date <= today:
            form.to_date.errors.append("Dates must be in the future!")
        elif from_date >= to_date:
            form.to_date.errors.append("Departure date must be after arrival date!")
        elif to_date > max_stay:
            form.to_date.errors.append("Departure date must within 20 days of arrival date!")
        elif from_date > max_date or to_date > max_date:
            form.from_date.errors.append("Dates must be within a year and a half of now!")

        else:
            from_date = from_date.strftime("%d/%m/%Y")
            to_date = to_date.strftime("%d/%m/%Y")

            session["booking"]["from_date"] = from_date
            session.modified = True
            session["booking"]["to_date"] = to_date
            session.modified = True
            return redirect(url_for('choose_destination'))
    return render_template("booking_choose_date.html", form=form, style="booking.css")

@app.route("/choose_destination", methods=["GET", "POST"])
@not_main_admin_required
def choose_destination():
    redirect_to = check_dates()
    if redirect_to is not None:
        return redirect_to
    
    form = ChooseDestinationForm()
    db = get_db()
    form.destination.choices = [city["city_name"] for city in db.execute("""SELECT * FROM destinations""").fetchall()]

    if form.validate_on_submit():
        destination = form.destination.data
        session["booking"]["destination"] = destination
        session.modified = True
        return redirect(url_for('choose_flight'))
    return render_template("booking_choose_destination.html", form=form, style="booking.css")

@app.route("/choose_flight", methods=["GET", "POST"])
@not_main_admin_required
def choose_flight():
    redirect_to = check_destination()
    if redirect_to is not None:
        return redirect_to
    
    form = ChooseFlightRouteForm()
    db = get_db()
    form.to_city.data = session["booking"]["destination"]
    form.from_city.choices = [city["from_city"] for city in db.execute("""SELECT DISTINCT from_city FROM routes WHERE to_city = ?;""", 
                                                                       (session["booking"]["destination"],)).fetchall()]
    if form.validate_on_submit():
        from_city = form.from_city.data
        session["booking"]["flight"]["from_city"] = from_city
        session.modified = True

        session["booking"]["flight"]["to_city"] = session["booking"]["destination"]
        session.modified = True
        return redirect(url_for('choose_airline'))
    return render_template("booking_choose_flight.html", form=form, style="booking.css")

@app.route("/choose_airline", methods=["GET", "POST"])
@not_main_admin_required
def choose_airline():
    redirect_to = check_flight_route()
    if redirect_to is not None:
        return redirect_to
    
    form = ChooseAirlineForm()
    db = get_db()
    form.airline.choices = [route["airline_name"] for route in db.execute("""SELECT * FROM routes WHERE from_city = ? AND to_city = ?;""",
                                                                          (session["booking"]["flight"]["from_city"], 
                                                                           session["booking"]["flight"]["to_city"])).fetchall()]
    if form.validate_on_submit():
        airline = form.airline.data
        session["booking"]["flight"]["airline"] = airline
        session.modified = True
        return redirect(url_for('choose_seats'))
    return render_template("booking_choose_airline.html", form=form, style="booking.css")

@app.route("/choose_seats", methods=["GET", "POST"])
@not_main_admin_required
def choose_seats():
    redirect_to = check_airline()
    if redirect_to is not None:
        return redirect_to
    
    form = ChooseSeatsForm()
    message = "Disclaimer: Prices shown are for single tickets. Return tickets have a mark-up of approx. 10 percent and will be added automatically."
    db = get_db()
    route = db.execute("""SELECT * FROM routes WHERE route_id = (SELECT route_id FROM routes WHERE from_city = ? AND to_city = ? AND airline_name = ?);""",
               (session["booking"]["flight"]["from_city"], session["booking"]["flight"]["to_city"], session["booking"]["flight"]["airline"])).fetchone()
    session["booking"]["flight"]["route_id"] = route["route_id"]
    session.modified = True
    available_eco = route["available_eco"]
    available_bus = route["available_bus"]
    available_fc = route["available_fc"]

    price_eco = route["price_eco"]
    price_bus = route["price_bus"]
    price_fc = route["price_fc"]

    duration = route["duration"]
    flight_hrs = duration // 60
    flight_mins = duration % 60

    if available_eco < 5:
        form.num_eco_tix.choices = [choice for choice in range(available_eco+1)]
    if available_bus < 4:
        form.num_bus_tix.choices = [choice for choice in range(available_bus+1)]
    if available_fc < 3:
        form.num_fc_tix.choices = [choice for choice in range(available_fc+1)]

    if form.validate_on_submit():
        num_eco_tix = int(form.num_eco_tix.data)
        num_bus_tix = int(form.num_bus_tix.data)
        num_fc_tix = int(form.num_fc_tix.data)

        if num_eco_tix == 0 and num_bus_tix == 0 and num_fc_tix == 0:
            form.num_fc_tix.errors.append("You must buy tickets!")
        else:
            session["booking"]["flight"]["tickets"]["num_eco_tix"] = num_eco_tix
            session.modified = True
            session["booking"]["flight"]["tickets"]["num_bus_tix"] = num_bus_tix
            session.modified = True
            session["booking"]["flight"]["tickets"]["num_fc_tix"] = num_fc_tix
            session.modified = True

            eco_cost = price_eco * num_eco_tix
            bus_cost = price_bus * num_bus_tix
            fc_cost = price_fc * num_fc_tix

            session["booking"]["flight"]["cost"] = (eco_cost * 2 + eco_cost//10)+(bus_cost * 2 + bus_cost//10)+(fc_cost * 2 + fc_cost//10)
            session.modified = True
            session["booking"]["cost"] += session["booking"]["flight"]["cost"]
            session.modified = True
            return redirect(url_for('choose_hotel'))
    return render_template("booking_choose_seats.html",
            form=form, price_eco=price_eco, price_bus=price_bus, price_fc=price_fc, message=message, flight_hrs=flight_hrs, flight_mins=flight_mins, style="booking.css")

@app.route("/choose_hotel", methods=["GET", "POST"])
@not_main_admin_required
def choose_hotel():
    redirect_to = check_seats()
    if redirect_to is not None:
        return redirect_to
    
    form = ChooseHotelForm()
    db =get_db()
    form.hotel.choices = [hotel["hotel_name"] for hotel in db.execute("""SELECT * FROM hotels AS h JOIN is_located_in AS isi JOIN destinations AS d
                                                                            ON h.hotel_id = isi.hotel_id AND isi.city_id = d.city_id
                                                                      WHERE d.city_name = ?;""", (session["booking"]["destination"],)).fetchall()]
    if form.validate_on_submit():
        hotel = form.hotel.data
        session["booking"]["hotel"]["hotel_name"] = hotel
        session.modified = True
        return redirect(url_for('choose_rooms'))
    return render_template("booking_choose_hotel.html", form=form, style="booking.css")

@app.route("/choose_rooms", methods=["GET", "POST"])
@not_main_admin_required
def choose_rooms():
    redirect_to = check_hotel()
    if redirect_to is not None:
        return redirect_to
    
    form = ChooseRoomsForm()
    db = get_db()
    hotel = db.execute("""SELECT * FROM hotels WHERE hotel_name = ?;""", (session["booking"]["hotel"]["hotel_name"],)).fetchone()
    
    session["booking"]["hotel_id"] = hotel["hotel_id"]
    session.modified = True

    available_2s = hotel["available_2s"]
    available_3s = hotel["available_3s"]
    available_1d = hotel["available_1d"]
    available_2d = hotel["available_2d"]
    available_1d1s = hotel["available_1d1s"]

    price_2s = hotel["price_2s"]
    price_3s = hotel["price_3s"]
    price_1d = hotel["price_1d"]
    price_2d = hotel["price_2d"]
    price_1d1s = hotel["price_1d1s"]

    if available_2s < 2:
        form.num_2s.choices = [choice for choice in range(available_2s+1)]
    if available_3s < 2:
        form.num_3s.choices = [choice for choice in range(available_3s+1)]
    if available_1d < 2:
        form.num_1d.choices = [choice for choice in range(available_1d+1)]
    if available_2d < 2:
        form.num_2d.choices = [choice for choice in range(available_2d+1)]
    if available_1d1s < 2:
        form.num_1d1s.choices = [choice for choice in range(available_1d1s+1)]    

    if form.validate_on_submit():
        num_2s = int(form.num_2s.data)
        num_3s = int(form.num_3s.data)
        num_1d = int(form.num_1d.data)
        num_2d = int(form.num_2d.data)
        num_1d1s = int(form.num_1d1s.data)

        if num_2s == 0 and num_3s == 0 and num_1d == 0 and num_2d == 0 and num_1d1s == 0:
            form.num_1d1s.errors.append("You must buy a room!")
        else:
            session["booking"]["hotel"]["rooms"]["num_2s_rooms"] = num_2s
            session.modified = True
            session["booking"]["hotel"]["rooms"]["num_3s_rooms"] = num_3s
            session.modified = True
            session["booking"]["hotel"]["rooms"]["num_1d_rooms"] = num_1d
            session.modified = True
            session["booking"]["hotel"]["rooms"]["num_2d_rooms"] = num_2d
            session.modified = True
            session["booking"]["hotel"]["rooms"]["num_1d1s_rooms"] = num_1d1s
            session.modified = True

            stay_length = session["booking"]["holiday_length"]

            cost_2s = price_2s * num_2s * stay_length
            cost_3s = price_3s * num_3s * stay_length
            cost_1d = price_1d * num_1d * stay_length
            cost_2d = price_2d * num_2d * stay_length
            cost_1d1s = price_1d1s * num_1d1s * stay_length

            session["booking"]["hotel"]["cost"] = (cost_2s * 2 + cost_2s//10)+(cost_3s * 2 + cost_3s//10)+(cost_1d * 2 + cost_1d//10)+(cost_2d * 2 + cost_2d//10)+(cost_1d1s * 2 + cost_1d1s//10)
            session.modified = True
            session["booking"]["cost"] += session["booking"]["hotel"]["cost"]
            session.modified = True
            return redirect(url_for('confirm_booking'))
    return render_template("booking_choose_rooms.html",
            form=form, price_2s=price_2s, price_3s=price_3s, price_1d=price_1d, price_2d=price_2d, price_1d1s=price_1d1s, style="booking.css")

@app.route("/confirm_booking", methods=["GET", "POST"])
@not_main_admin_required
def confirm_booking():
    redirect_to = check_rooms()
    if redirect_to is not None:
        return redirect_to
    
    form = ConfirmBookingForm()
    db = get_db()

    if form.validate_on_submit():
        confirm = form.confirm.data
        if confirm == "Restart":
            return redirect(url_for('choose_dates'))
        else:
            db.execute("""INSERT INTO flight_bookings (user_id, route_id, dep_date,
                       num_eco_tix, num_bus_tix, num_fc_tix, flight_cost)
                       VALUES (?,?,?,?,?,?,?);""", (g.user_id, session["booking"]["flight"]["route_id"], session["booking"]["from_date"], 
                        session["booking"]["flight"]["tickets"]["num_eco_tix"], session["booking"]["flight"]["tickets"]["num_bus_tix"],
                        session["booking"]["flight"]["tickets"]["num_fc_tix"], session["booking"]["flight"]["cost"]))
            db.commit()

            db.execute("""INSERT INTO hotel_bookings (user_id, hotel_id, arr_date, dep_date,
                       num_2s_rooms, num_3s_rooms, num_1d_rooms, num_2d_rooms, num_1d1s_rooms, hotel_cost)
                       VALUES (?,?,?,?,?,?,?,?,?,?);""", (g.user_id, session["booking"]["hotel_id"], session["booking"]["from_date"],
                        session["booking"]["to_date"], session["booking"]["hotel"]["rooms"]["num_2s_rooms"], session["booking"]["hotel"]["rooms"]["num_3s_rooms"],
                        session["booking"]["hotel"]["rooms"]["num_1d_rooms"], session["booking"]["hotel"]["rooms"]["num_2d_rooms"],
                        session["booking"]["hotel"]["rooms"]["num_1d1s_rooms"], session["booking"]["hotel"]["cost"]))
            db.commit()

            route = db.execute("""SELECT * FROM routes WHERE route_id = ?;""", (session["booking"]["flight"]["route_id"],)).fetchone()
            available_eco = route["available_eco"]
            available_bus = route["available_bus"]
            available_fc = route["available_fc"]
            db.execute("""UPDATE routes SET available_eco = ?, available_bus = ?, available_fc = ? WHERE route_id = ?;""",
                       (available_eco-session["booking"]["flight"]["tickets"]["num_eco_tix"],
                        available_bus-session["booking"]["flight"]["tickets"]["num_bus_tix"],
                        available_fc-session["booking"]["flight"]["tickets"]["num_fc_tix"],
                        session["booking"]["flight"]["route_id"]))
            db.commit()

            hotel = db.execute("""SELECT * FROM hotels WHERE hotel_id = ?;""", (session["booking"]["hotel_id"],)).fetchone()
            available_2s = hotel["available_2s"]
            available_3s = hotel["available_3s"]
            available_1d = hotel["available_1d"]
            available_2d = hotel["available_2d"]
            available_1d1s = hotel["available_1d1s"]
            db.execute("""UPDATE hotels SET available_2s = ?, available_3s = ?, available_1d = ?, available_2d = ?, available_1d1s = ? WHERE hotel_id = ?;""",
                       (available_2s-session["booking"]["hotel"]["rooms"]["num_2s_rooms"],
                        available_3s-session["booking"]["hotel"]["rooms"]["num_3s_rooms"],
                        available_1d-session["booking"]["hotel"]["rooms"]["num_1d_rooms"],
                        available_2d-session["booking"]["hotel"]["rooms"]["num_2d_rooms"],
                        available_1d1s-session["booking"]["hotel"]["rooms"]["num_1d1s_rooms"],
                        session["booking"]["hotel_id"]))
            db.commit()

            return redirect(url_for('home_page'))
    return render_template("confirm_booking.html", form=form, style="booking.css")


@app.route("/make_admin", methods=["GET", "POST"])
@admin_required
def make_admin():
    form = MakeAdminForm()
    db = get_db()

    form.user.choices = [user["user_id"] for user in db.execute("""SELECT * FROM users""")]

    if form.validate_on_submit():
        user = form.user.data

        db.execute("""UPDATE users SET is_admin = 1 WHERE user_id = ?;""", (user,))
        db.commit()
    return render_template("make_admin.html", form=form)

@app.route("/remove_admin", methods=["GET", "POST"])
@admin_required
def remove_admin():
    form = MakeAdminForm()
    db = get_db()

    form.user.choices = [user["user_id"] for user in db.execute("""SELECT * FROM users WHERE is_admin = 1""")]

    if form.validate_on_submit():
        user = form.user.data
        if user == "admin":
            return(redirect(url_for('admin')))
        else:
            db.execute("""UPDATE users SET is_admin = 0 WHERE user_id = ?;""", (user,))
            db.commit()
    return render_template("make_admin.html", form=form)

#add tickets
#add rooms
#add/remove admin status
#wishlist
