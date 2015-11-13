"""Server file for law school application tool project."""

# import jinja debugging tool
from jinja2 import StrictUndefined
# import flask tools
from flask import Flask, render_template, redirect, request, flash, session, jsonify
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
    # get all schools & their info
    schools = School.query.all()

    if session:
        # id schools user has added to their list
        user_schools = list_selected_schools()

        # compare user stats to school stats & return list of categorized matches
        list_of_schools = compare_user_stats()

        # divide out list_of_schools into more usable variables
        safety_schools = list_of_schools[0]
        match_schools = list_of_schools[1]
        stretch_schools = list_of_schools[2]
        split_schools = list_of_schools[3]

    else:
        # if user not in session, pass in blank data
        user_schools = []
        safety_schools = []
        match_schools = []
        stretch_schools = []
        split_schools = []

    return render_template("schools.html",
                           schools=schools,
                           user_schools=user_schools,
                           safety_schools=safety_schools,
                           match_schools=match_schools,
                           stretch_schools=stretch_schools,
                           split_schools=split_schools)


@app.route('/schools/<int:school_id>')
def display_school_data(school_id):
    """Display profile page & data for individual law school."""
    school = School.query.get(school_id)

    # if user is in session, get their selected schools and categorized matches
    if session:
        # id schools user has added to their list
        user_schools = list_selected_schools()

        # compare user stats to school stats & return list of categorized matches
        list_of_schools = compare_user_stats()

        # divide out list_of_schools into more usable variables
        safety_schools = list_of_schools[0]
        match_schools = list_of_schools[1]
        stretch_schools = list_of_schools[2]
        split_schools = list_of_schools[3]

    else:
        # if user not in session, pass in blank data
        user_schools = []
        safety_schools = []
        match_schools = []
        stretch_schools = []
        split_schools = []

    return render_template("school_profile.html",
                           school=school,
                           user_schools=user_schools,
                           safety_schools=safety_schools,
                           match_schools=match_schools,
                           stretch_schools=stretch_schools,
                           split_schools=split_schools)


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

        # return all db data needed for display on user list
        # School.address is for basic display and possibly gmaps later
        # School.gpa and School.lsat are for comparing to user stats w chart.js later
        school_list = db.session.query(School.school_name,
                                       School.address,
                                       School.gpa_75,
                                       School.gpa_50,
                                       School.gpa_25,
                                       School.lsat_75,
                                       School.lsat_50,
                                       School.lsat_25,
                                       School_list.user_id,
                                       School_list.school_id,
                                       School_list.admission_chance,
                                       School_list.app_submitted
                                       ).filter(School_list.user_id == user_id).join(School_list).order_by(School.school_name).all()

        return render_template("user_profile.html", user=user, school_list=school_list)


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
    """Return list of schools matching user gpa and lsat scores"""

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

        # identify schools already in user list
        user_schools = list_selected_schools()

        # categorize schools as compared to user stats
        list_of_schools = compare_user_stats()

        # separate out results of query into variables
        safety_schools = list_of_schools[0]
        match_schools = list_of_schools[1]
        stretch_schools = list_of_schools[2]
        split_schools = list_of_schools[3]

    return render_template("school_match.html",
                           user_gpa=user_gpa,
                           user_lsat=user_lsat,
                           user_schools=user_schools,
                           safety_schools=safety_schools,
                           match_schools=match_schools,
                           stretch_schools=stretch_schools,
                           split_schools=split_schools)


@app.route('/add_school_to_list', methods=['POST'])
def add_school_to_list():
    """Add user's selected school as row in School_list"""
    # get user_id from session
    user_id = session['user_id']
    # get other db data from post request
    school_id = request.form.get("school_id")
    admission_chance = request.form.get("admission_chance")

    # check if school already selected by user
    if School_list.query.filter_by(user_id=user_id, school_id=school_id).first():
        print "It's already there!"
        return jsonify({user_id: school_id})

    # add new list item to School_list & commit to db
    else:
        new_list_item = School_list(user_id=user_id,
                                    school_id=school_id,
                                    admission_chance=admission_chance,
                                    app_submitted=False)

        db.session.add(new_list_item)
        db.session.commit()

        print "added to db"
        return jsonify({user_id: school_id})


@app.route('/update_user_gpa.json', methods=['POST'])
def update_user_gpa():
    """Update user's GPA in database & return data as JSON object."""
    user_id = session['user_id']
    gpa = request.form.get("gpa")

    # match user in session to user record in db & rewrite gpa in db
    user = User.query.filter_by(user_id=user_id).first()
    user.gpa = gpa
    db.session.commit()

    return jsonify({"gpa": gpa})


@app.route('/update_user_lsat.json', methods=['POST'])
def update_user_lsat():
    """Update user's LSAT score in database & return data as JSON object."""
    user_id = session['user_id']
    lsat = request.form.get("lsat")

    # match user in session to user record in db & rewrite lsat in db
    user = User.query.filter_by(user_id=user_id).first()
    user.lsat = lsat
    db.session.commit()

    return jsonify({"lsat": lsat})


@app.route('/update_app_submission.json', methods=['POST'])
def update_app_submission():
    """Update user's app submission status for one school & return data as JSON object"""
    user_id = session['user_id']
    school_id = request.form.get("school_id")

    # find School_list row for user/school
    school_choice = School_list.query.filter_by(user_id=user_id, school_id=school_id).first()

    # change boolean value of field to 1 & write to db
    school_choice.app_submitted = 1
    db.session.commit()

    return jsonify({"school_id": school_id})


@app.route('/remove_school.json', methods=['POST'])
def remove_school_from_list():
    """Remove a school from user's list of selected schools"""
    user_id = session['user_id']
    school_id = request.form.get("school_id")

    # find School_list row for user/school
    school_choice = School_list.query.filter_by(user_id=user_id, school_id=school_id).first()
    print school_choice

    # remove school_choice from db
    db.session.delete(school_choice)
    db.session.commit()

    # return something w jsonify
    return jsonify({"school_removed": school_id})


@app.route('/display_user_school_list')
def display_user_school_list():
    pass
    # currently doing a basic version of this in profile route
    # to display list, need different route w query to find & return user's choices
    # consider whether to just delete this: probably


# Helper functions

def compare_user_stats():
    """Find safety, match, stretch, and split schools for logged-in user"""
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
        split_schools = School.id_split_schools(user_gpa, user_lsat)

    elif user_gpa and not user_lsat:
        # return query results for gpa alone
        safety_schools = School.id_safety_schools_gpa(user_gpa)
        match_schools = School.id_match_schools_gpa(user_gpa)
        stretch_schools = School.id_stretch_schools_gpa(user_gpa)
        split_schools = []

    elif user_lsat and not user_gpa:
        # return query results for lsat score alone
        safety_schools = School.id_safety_schools_lsat(user_lsat)
        match_schools = School.id_match_schools_lsat(user_lsat)
        stretch_schools = School.id_stretch_schools_lsat(user_lsat)
        split_schools = []

    return [safety_schools, match_schools, stretch_schools, split_schools]


def list_selected_schools():
    """Gets all schools selected by user and converts into list."""
    # id schools user has already added to their list
    schools_in_lists = db.session.query(School_list.school_id)
    school_tuples = schools_in_lists.filter(School_list.user_id == session['user_id']).all()
    # transform list of tuples into basic list
    selected_schools = [i[0] for i in school_tuples]

    return selected_schools


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
