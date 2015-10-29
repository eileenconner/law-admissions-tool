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


@app.route('/schools')
def list_schools():
    """Alphabetical list of all schools in database."""
    schools = School.query.all()
    return render_template("schools.html", schools=schools)


@app.route('/login')
def login():
    """Log in to app."""
    pass


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
