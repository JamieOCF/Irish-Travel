from flask import Flask, render_template, redirect, url_for, session, g
from database import get_db, close_db 
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from forms import RegistrationForm, LoginForm
from forms import CompaniesForm, DestinationsForm


app = Flask(__name__)
app.config.from_pyfile("config.py")
Session(app)
app.teardown_appcontext(close_db)



@app.before_request
def load_logged_in_user():
    username = session.get("username", None)

    if username is not None:
        db = get_db()
        user = db.execute("""SELECT * FROM users WHERE username = ?;""", (username,)).fetchone()
        if user is not None:
            if user["access_level"] == 1:
                session["access_level"] = 1
                session.modified = True
                g.is_admin = True
                g.username = user["username"]
            else:
                session["access_level"] == 0
                g.is_admin = False
                g.username = user["username"]
    else:
        session["access_level"] = 0
        session["username"] = None
        session.modified = True



#########################
#WRAPPERS
#########################
def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if session["username"] == None:
            return redirect(url_for("home_page"))
        elif session["access_level"] == 0:
            return redirect(url_for("user"))
        return view(*args, **kwargs)
    return wrapped_view

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if session["username"] == None:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view



#########################
#BASE ROUTES
#########################
@app.route("/")
def home_page():
    session["url"] = url_for("home_page")
    session.modified = True
    return render_template("pages/home_page.html", style="home.css")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = get_db()
        clash = db.execute("""SELECT * FROM users WHERE username = ?;""",
                           (username,)).fetchone()
        if clash is not None:
            form.username.errors.append("Username already taken!")
        elif username.lower() == "admin":
            form.username.errors.append("Try different username!")
        else:
            db.execute("""INSERT INTO users (username, password, access_level)
                       VALUES (?, ?, ?);""", (username, generate_password_hash(password), 0))
            db.commit()
            return redirect(url_for("login"))
    return render_template("auth/register.html", style="auth.css", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = get_db()
        user_in_db = db.execute("""SELECT * FROM users WHERE username = ?;""",
                   (username,)).fetchone()
        if user_in_db is None or not check_password_hash(user_in_db["password"], password):
            form.username.errors.append("Username or password is incorrect!")
        else:
            session["username"] = username
            username = user_in_db["username"]
            session.modified = True
            g.username = username
            next_page = session["url"]
            if not next_page:
                next_page = url_for("home_page")
            return redirect(next_page)
    return render_template("auth/login.html", style="auth.css", form=form)

@app.route("/logout")
def logout():
    session.clear()
    session.modified = True
    return redirect(url_for("home_page"))



#########################
#BOOKING
#########################
@app.route("/booking")
def book():
    session["url"] = url_for("book")
    session.modified = True
    return render_template("booking/booking.html")


#########################
#SHOWCASES
#########################
@app.route("/destinations")
def destinations():
    session["url"] = url_for("destinations")
    session.modified = True
    db = get_db()
    destinations = db.execute("""SELECT * FROM destinations""")
    return render_template("pages/destinations.html", destinations=destinations)

@app.route("/hotels")
def hotels():
    session["url"] = url_for("hotels")
    session.modified = True
    db = get_db()
    hotels = db.execute("""SELECT * FROM hotels""")
    return render_template("pages/hotels.html", hotels=hotels)

@app.route("/wishlist")
@login_required
def wishlist():
    session["url"] = url_for("wishlist")
    session.modified = True
    if session["username"] is None:
        return redirect(url_for("login"))
    return render_template("pages/wishlist.html")



#########################
#ACCOUNT PANELS
#########################
@app.route("/admin")
@admin_required
def admin():
    return render_template("users/admin.html", style="admin.css")

@app.route("/user")
@login_required
def user():
    return render_template("users/user.html")



#########################
#ADMIN PAGES
#########################
@app.route("/admin/guide")
@admin_required
def guide():
    return render_template("admin/guide.html")

#bookings
@app.route("/admin/bookings")
@admin_required
def bookings():
    return render_template("admin/bookings.html")

@app.route("/admin/tickets")
@admin_required
def tickets():
    return render_template("admin/tickets.html")

@app.route("/admin/wishlists")
@admin_required
def wishlists():
    return render_template("admin/wishlists.html")

#destinations
@app.route("/admin/manage_destinations", methods={"GET","POST"})
@admin_required
def manage_destinations():
    form = DestinationsForm()
    db = get_db()
    alldestinations = db.execute("""SELECT * FROM destinations""").fetchall()
    if form.validate_on_submit():
        city_name = str(form.city_name.data).title()
        country = str(form.country.data).title()
        clash = db.execute("""SELECT * FROM destinations WHERE city_name = ? AND country = ?;""",
                           (city_name,country,)).fetchone()
        if clash is not None:
            form.city_name.errors.append("Destination already exists!")
        else:
            db.execute("""INSERT INTO destinations (city_name, country)
                       VALUES (?, ?);""", (city_name, country,))
            db.commit()
            return redirect(url_for('manage_destinations'))
    return render_template("admin/manage_destinations.html", alldestinations=alldestinations)

#hotels
@app.route("/admin/manage_hotels")
@admin_required
def manage_hotels():
    return render_template("admin/manage_hotels.html")

@app.route("/admin/room_types")
@admin_required
def room_types():
    return render_template("admin/room_types.html")

@app.route("/admin/rooms")
@admin_required
def rooms():
    return render_template("admin/rooms.html")

#routes
@app.route("/admin/manage_routes")
@admin_required
def manage_routes():
    return render_template("admin/manage_routes.html")

@app.route("/admin/fare_classes")
@admin_required
def fare_classes():
    return render_template("admin/fare_classes.html")

@app.route("/admin/rides")
@admin_required
def rides():
    return render_template("admin/rides.html")

#companies
@app.route("/admin/companies", methods={"GET","POST"})
@admin_required
def companies():
    form = CompaniesForm()
    db = get_db()
    allcompanies = db.execute("""SELECT * FROM companies""").fetchall()
    if form.validate_on_submit():
        company_name = str(form.company_name.data).title()
        transport_mode = form.transport_mode.data
        clash = db.execute("""SELECT * FROM companies WHERE company_name = ?;""",
                           (company_name,)).fetchone()
        if clash is not None:
            form.company_name.errors.append("Name already taken!")
        else:
            db.execute("""INSERT INTO companies (company_name, transport_mode)
                       VALUES (?, ?);""", (company_name, transport_mode,))
            db.commit()
            return redirect(url_for('companies'))
    return render_template("admin/companies.html", form=form, allcompanies=allcompanies, style="companies.css")



#########################
#FEEDBACK
#########################
@app.route("/review")
@login_required
def review():
    return render_template("feedback/review.html")

@app.route("/report")
@login_required
def report():
    return render_template("feedback/report.html")