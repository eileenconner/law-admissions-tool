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
        # pull out user data for logged-in user & feed into template
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
    # if gpa or lsat fields are blank, set to None
    try:
        gpa = float(request.form['gpa'])
    except:
        gpa = None
    try:
        lsat = int(request.form['lsat'])
    except:
        lsat = None

    # check whether user is already in db and redirect to /login if needed
    if User.query.filter_by(email=email).first():
        flash("You are already registered. Please login to continue.")
        return redirect('/login')

    else:
        # create user instance with form values
        new_user = User(email=email, password=password, gpa=gpa, lsat=lsat)

        # write user data to database
        db.session.add(new_user)
        db.session.commit()

        # send confirmation message and proceed to login
        flash("You are now registered and may login.")
        return redirect('/login')


# Main site routes for db query and return

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

        # return results by gpa and lsat, gpa only, or lsat only, depending on user stats
        if user_gpa and user_lsat:
            # return query match for gpa and lsat score
            safety_schools = School.id_safety_schools(user_gpa, user_lsat)
            match_schools = School.id_match_schools(user_gpa, user_lsat)
            stretch_schools = School.id_stretch_schools(user_gpa, user_lsat)
            # add when split_schools functionality working:
            #split_schools = School.id_split_schools(user_gpa, user_lsat)

            return render_template("school_match.html",
                                   user_gpa=user_gpa,
                                   user_lsat=user_lsat,
                                   safety_schools=safety_schools,
                                   match_schools=match_schools,
                                   stretch_schools=stretch_schools,)
                                   #split_schools=split_schools)

        # consider how to fit the content of these two elifs into a single
        # template: school_match.html (jinja if/else? likely)
        # here nest if/elif/elif and return render_template.html at the end
        # then add jinja if/else functionality to display in template

        elif user_gpa and not user_lsat:
            # return query results for gpa alone
            safety_schools = School.id_safety_schools_gpa(user_gpa)
            match_schools = School.id_match_schools_gpa(user_gpa)
            stretch_schools = School.id_stretch_schools_gpa(user_gpa)

            return render_template("school_match_gpa.html",
                                   user_gpa=user_gpa,
                                   safety_schools=safety_schools,
                                   match_schools=match_schools,
                                   stretch_schools=stretch_schools,)

        elif user_lsat and not user_gpa:
            # return query results for lsat score alone
            safety_schools = School.id_safety_schools_lsat(user_lsat)
            match_schools = School.id_match_schools_lsat(user_lsat)
            stretch_schools = School.id_stretch_schools_lsat(user_lsat)

            return render_template("school_match_lsat.html",
                                   user_lsat=user_lsat,
                                   safety_schools=safety_schools,
                                   match_schools=match_schools,
                                   stretch_schools=stretch_schools,)


@app.route('/add_school_to_list', methods=['POST'])
def add_school_to_list():
    """Add user's selected school as row in School_list"""
    # get user_id from session
    user_id = session['user_id']
    # get other db data from post request
    school_id = request.form.get("school_id")
    admission_chance = request.form.get("admission_chance")

    return " "

    # need to check whether user has already added school & remove ability to add if so
    # this will probably go in school_match.html
    # and disable button if user has already added school to list
    # gray out button/no longer addable: do w successhandler in html/ajax
    # for now use simple if/else w/ query to ensure user/school id combo isn't in School_list

    # tested below w multiple clicks. appeared to add multiple times, but there's only one post!

    # if School_list.query.filter_by(user_id=user_id, school_id=school_id).first():
    #     return "It's already there!"

    # # else:
    #     new_list_item = School_list(user_id=user_id,
    #                                 school_id=school_id,
    #                                 admission_chance=admission_chance,
    #                                 app_submitted=False)

    #     db.session.add(new_list_item)
    #     db.session.commit()

    #     return " "


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
