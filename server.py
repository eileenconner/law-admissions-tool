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
def login():
    """Log in to app."""
    pass
    return render_template("login.html")


@app.route('/profile')
def display_profile():
    """Display user profile."""
    pass
    return render_template("profile.html")


# v.2?
# @app.route('/register')
# def register():
#     """Register for site."""
#     pass
#     return render_template("register.html")


# Main site routes for db query and return

@app.route('/school_query')
def match_gpa_and_lsat():
    pass
    # pass in user's gpa and lsat scores
    # compare scores against each school's GPA/LSAT
    # results differ depending on whether user wants to compare to 25th. 50th, 75th %ile
    # if/else loop to match according to user's gpa, lsat, or both gpa and lsat,
    # return list of schools whose scores most closely match user's stats
    # list should be ordered by closeness to user scores (abs?) beginning with exact matches
    # each item in list should have:
    # - school name w dynamically generated link to profile page
    # - school scores for gpa match OR lsat match OR both (v2: colored/numbered stars)
    # - button to add school to my list
    # onclick of button --> should be its own rute




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
