"""Server file for law school application tool project."""

# import jinja debugging tool
from jinja2 import StrictUndefined

# import flask tools
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

# Import database & classes from model.py
from model import connect_to_db, db, School, User, School_list


# make it a Flask app!
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "itsasecret"

# raise errors for jinja bugs
app.jinja_env.undefined = StrictUndefined


# Routes!

@app.route('/')
def index():
    """Homepage."""
    return render_template("index.html")


# Law school data display routes

@app.route('/schools')
def list_schools():
    """Alphabetical list of all schools in database."""
    schools = School.query.all()
    return render_template("schools.html", schools=schools)


@app.route('/schools/<int:school_id>')
def display_school_data(school_id):
    """Display profile page & data for individual law school"""
    school = School.query.get(school_id)
    return render_template("school_profile.html", school=school)


# User-related routes: login, registration, profile

@app.route('/login')
def login_form():
    """Render login form."""
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
    """Log in to app."""
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    # Check if user is in db and if password is correct
    if not user:
        flash("You are not registered as a user.")
        return redirect('/login')
    if user.password != password:
        flash("Incorrect password.")
        return redirect('/login')

    # Add user to session & display message
    session['user_id'] = user.user_id
    flash("You have logged in.")
    return redirect('/')


@app.route('/logout')
def logout():
    """Log out of app."""
    # Delete user id from session & display message
    del session['user_id']
    flash('You have logged out.')
    return redirect('/')


@app.route('/profile')
def display_profile():
    """Display user profile."""
    # Check if user is logged in before querying; redirect to login page if needed
    if not session:
        flash("You must login to continue.")
        return redirect('/login')
    else:
        # pull out user data for logged-in user
        user_id = session['user_id']
        user = User.query.filter_by(user_id=user_id).first()
        return render_template("user_profile.html", user=user)


@app.route('/register')
def register():
    """Direct user to site registration."""
    return render_template("registration.html")


@app.route('/register', methods=['POST'])
def add_user_to_db():
    """Register new user: process user information and write to database."""
    # get user info from form
    email = request.form['email']
    password = request.form['password']
    gpa = float(request.form['gpa'])
    lsat = int(request.form['lsat'])

    # create user instance with form values
    new_user = User(email=email, password=password, gpa=gpa, lsat=lsat)

    # write user data to database
    db.session.add(new_user)
    db.session.commit()

    # send confirmation message and proceed to login
    flash("You are now registered and may login.")
    return redirect('/login')


# Main site routes for db query and return

@app.route('/school_query_gpa')
def match_gpa():
    """Return list of schools with 50th percentile gpa lower than the user's gpa"""

    # Check if user is logged in before querying; redirect to login page if needed
    if not session:
        flash("You must login to continue.")
        return redirect('/login')
    else:
        # Pull out gpa datapoint for user currently logged in
        user_id = session['user_id']
        user = User.query.filter_by(user_id=user_id).first()
        user_gpa = user.gpa

        # Find list of schools by comparing against user gpa
        gpa_matched_schools = School.query.filter(user_gpa > School.gpa_50).order_by(School.gpa_50.desc()).all()

        return render_template("gpa_match.html", gpa_matched_schools=gpa_matched_schools)

    # pass in user_gpa as argument to function (from user session data)
    # compare gpa against each school's GPA_50% point
    # (LATER: results differ depending on whether user wants to compare to 25th, 50th, 75th %ile)
    # return list of schools whose scores most closely match user's stats
    # list should be ordered by gpa_50: difference between user score and school gpa?
    # or just order results smallest to largest (or reverse if it makes most sense)
    # each item in list should have:
    # - school name w dynamically generated link to profile page
    # - school scores for gpa match (LATER both gpa & lsat (v2: colored/numbered stars))
    # - button/link to add school to my list


@app.route('/school_query_lsat')
def match_lsat():
    """return list of schools with 50th percentile lsat lower than the user's lsat"""

    # Check if user is logged in before querying; redirect to login page if needed
    if not session:
        flash("You must login to continue.")
        return redirect('/login')
    else:
        # Pull out lsat datapoint for user currently logged in
        user_id = session['user_id']
        user = User.query.filter_by(user_id=user_id).first()
        user_lsat = user.lsat

        lsat_matched_schools = School.query.filter(user_lsat > School.lsat_50).order_by(School.lsat_50.desc()).all()

        return render_template("lsat_match.html", lsat_matched_schools=lsat_matched_schools)


@app.route('/school_query')
def match_law_schools():
    """Return list of schools matching both user gpa and user lsat scores"""

    # Check if user is logged in before querying; redirect to login page if needed
    if not session:
        flash("You must login to continue.")
        return redirect('/login')

    else:
        # Pull out gpa and lsat datapoints for user currently logged in
        user_id = session['user_id']
        user = User.query.filter_by(user_id=user_id).first()
        user_gpa = user.gpa
        user_lsat = user.lsat

        # consider when/whether to implement if/else.
        # if user_gpa and user_lsat:
        safety_schools = School.id_safety_schools(user_gpa, user_lsat)
        match_schools = School.id_match_schools(user_gpa, user_lsat)
        stretch_schools = School.id_stretch_schools(user_gpa, user_lsat)

        # add when split_schools functionality working:
        # split_schools = School.id_split_schools(user_gpa, user_lsat)

        return render_template("school_match.html",
                               user_gpa=user_gpa,
                               user_lsat=user_lsat,
                               safety_schools=safety_schools,
                               match_schools=match_schools,
                               stretch_schools=stretch_schools,)
                               # split_schools=split_schools)

        # if user_gpa and not user_lsat:
        #     pass
        # if not user_gpa and user_lsat:
        #     pass


@app.route('/add_school_to_list')
def add_school_to_list():
    pass
    # happens on click of button (displayed dynamically with each school listing)
    # adds school connected with that button to user list
    # how? ??
    # when user pushes the button, query should add that school/etc to School_list
    # with User.user_id and School.school.id.


@app.route('/display_user_school_list')
def display_user_school_list():
    pass
    # to display list, need different route w query to find & return user's choices


# do these things when running in console:
if __name__ == "__main__":

    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    # connect to the db
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(debug=True)
