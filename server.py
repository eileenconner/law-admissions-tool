"""Server file for law school application tool project."""

import json
# import jinja debugging tool
from jinja2 import StrictUndefined
# import flask tools
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
# Import database & classes from model.py
from model import connect_to_db, db, School, User, School_list
# import geopy tools for lat/long derivation from address data
from geopy.geocoders import GoogleV3


# make it a Flask app!
app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = "itsasecret"
# raise errors for jinja bugs
app.jinja_env.undefined = StrictUndefined


# Routes!

@app.route('/')
def index():
    """Returns homepage."""
    return render_template("index.html")


# Law school data display routes

@app.route('/schools')
def list_schools():
    """Displays alphabetical list of all schools in database."""
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
    """Displays profile page & data for individual law school."""
    school = School.query.get(school_id)

    # transform school.address into lat & long w geopy/GoogleV3
    # pass into template for js map generation
    geolocator = GoogleV3()
    address, (latitude, longitude) = geolocator.geocode(school.address)
    lat, lng = (latitude, longitude)

    # if user is in session, get their stats, selected schools, and categorized matches
    if session:
        # id user gpa and lsat
        user_stats = find_user_gpa_lsat()
        user_gpa = user_stats[0]
        user_lsat = user_stats[1]

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
                           lat=lat,
                           lng=lng,
                           user_gpa=user_gpa,
                           user_lsat=user_lsat,
                           user_schools=user_schools,
                           safety_schools=safety_schools,
                           match_schools=match_schools,
                           stretch_schools=stretch_schools,
                           split_schools=split_schools)


# User-related routes: login, registration, profile

@app.route('/login')
def login_form():
    """Renders login form."""
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
    """Logs in to app."""
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
    """Logs out of app."""
    # Delete user id from session & display message
    del session['user_id']
    flash('You have logged out.')
    return redirect('/')


@app.route('/profile')
def display_profile():
    """Displays user profile and list of selected law schools."""
    # Check if user is logged in before querying; redirect to login page if needed
    if not session:
        flash("You must login to continue.")
        return redirect('/login')
    else:
        # pull out user data for logged-in user & feed into template
        user_id = session['user_id']
        user = User.query.filter_by(user_id=user_id).first()

        # get all db data for schools selected by user in session
        school_list = query_user_schools(user_id)

        # get address, lat/long, and user admission chance for each school in list
        school_coords = identify_school_coords(school_list)

        # render template with all values included
        return render_template("user_profile.html",
                               user=user,
                               school_list=school_list,
                               school_coords=school_coords)


@app.route('/register')
def register():
    """Directs user to site registration."""
    return render_template("registration.html")


@app.route('/register', methods=['POST'])
def add_user_to_db():
    """Registers new user: processes user information and writes to database."""
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
    """Returns list of schools matching user gpa and lsat scores"""

    # Check if user is logged in before querying; redirect to login page if needed
    if not session:
        flash("You must login to continue.")
        return redirect('/login')

    else:
        # Pull out gpa and lsat datapoints for user currently logged in
        user_stats = find_user_gpa_lsat()
        user_gpa = user_stats[0]
        user_lsat = user_stats[1]

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
    """Adds user's selected school as row in School_list"""
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
    """Updates user's GPA in database & returns data as JSON object."""
    user_id = session['user_id']
    gpa = request.form.get("gpa")

    # match user in session to user record in db & rewrite gpa in db
    user = User.query.filter_by(user_id=user_id).first()
    user.gpa = gpa
    db.session.commit()

    return jsonify({"gpa": gpa})


@app.route('/update_user_lsat.json', methods=['POST'])
def update_user_lsat():
    """Updates user's LSAT score in database & returns data as JSON object."""
    user_id = session['user_id']
    lsat = request.form.get("lsat")

    # match user in session to user record in db & rewrite lsat in db
    user = User.query.filter_by(user_id=user_id).first()
    user.lsat = lsat
    db.session.commit()

    return jsonify({"lsat": lsat})


@app.route('/update_app_submission.json', methods=['POST'])
def update_app_submission():
    """Updates user's app submission status for one school & returns data as JSON object"""
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
    """Removes a school from user's list of selected schools"""
    user_id = session['user_id']
    school_id = request.form.get("school_id")

    # find School_list row for user/school
    school_choice = School_list.query.filter_by(user_id=user_id, school_id=school_id).first()

    # remove school_choice from db
    db.session.delete(school_choice)
    db.session.commit()

    return jsonify({"school_removed": school_id})

    # future to-dos:
    # regenerate list of schools/coords/adm chance for user in session
    # use this data to dynamically regenerate map markers in callback function

    # lst = school_list(user_id)
    # school_coords = identify_school_coords(lst)
    # return school_coords


@app.route('/admission_chance.json')
def count_admission_chance():
    """Finds # schools per admission category in user's selected schools and return for chart generation."""

    user_id = session['user_id']
    user_schools = School_list.query.filter_by(user_id=user_id).all()

    # count schools in each admission chance category and put in list
    # [0] safety [1] match [2] stretch [3] split [4] uncategorized
    adm_category_count = [0, 0, 0, 0, 0]

    for item in user_schools:
        if item.admission_chance == "Safety":
            adm_category_count[0] += 1
        elif item.admission_chance == "Match":
            adm_category_count[1] += 1
        elif item.admission_chance == "Stretch":
            adm_category_count[2] += 1
        elif item.admission_chance == "Split":
            adm_category_count[3] += 1
        else:
            adm_category_count[4] += 1

    # put data in usable dictionary
    data_cat_count = {
        'chance': [
            {
                "value": adm_category_count[0],
                "color": "#33cc33",
                "highlight": "#99e699",
                "label": "Safety"
            },
            {
                "value": adm_category_count[1],
                "color": "#ffff00",
                "highlight": "#ffff80",
                "label": "Match"
            },
            {
                "value": adm_category_count[2],
                "color": "#ff0000",
                "highlight": "#ff8080",
                "label": "Stretch"
            },
            {
                "value": adm_category_count[3],
                "color": "#6600ff",
                "highlight": "#b380ff",
                "label": "Split"
            },
            {
                "value": adm_category_count[4],
                "color": "#0099ff",
                "highlight": "#80ccff",
                "label": "Uncategorized"
            }
        ]
    }

    # return jsonified data to use in doughnut chart.js chart of school chance distribution
    return jsonify(data_cat_count)

    # future to-dos:
    # regenerate this chart dynamically when user removes school from list


# Helper functions

def compare_user_stats():
    """Finds safety, match, stretch, and split schools for logged-in user"""
    # Pull out gpa and lsat datapoints for user currently logged in
    user_stats = find_user_gpa_lsat()
    user_gpa = user_stats[0]
    user_lsat = user_stats[1]

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


def find_user_gpa_lsat():
    """Returns GPA and LSAT score of user in session as list."""
    user_id = session['user_id']
    user = User.query.filter_by(user_id=user_id).first()
    return [user.gpa, user.lsat]


def query_user_schools(user_id):
    """Returns data about each school in user's list of schools."""
    return db.session.query(School.school_name,
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


def identify_school_coords(school_list):
    """Returns address, lat/long, and user's admission chance for each school in school_list"""
    # initialize geolocator to pull out lat/long values
    geolocator = GoogleV3()

    # set up empty lists for return values for 1. map coordinates 2. admission category count
    school_coords = []

    for item in school_list:
        # get lat & long for each school address in school_list
        address, (latitude, longitude) = geolocator.geocode(item.address)
        lat, lng = (latitude, longitude)
        school = item.school_name
        admission_chance = item.admission_chance

        # add name, lat, lng to school_coords
        school_coords.append([school, lat, lng, admission_chance])

    return json.dumps(school_coords)


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
