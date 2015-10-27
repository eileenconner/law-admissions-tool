"""Models and database functions for law school admissions tool project."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


# Model definitions


class School(db.Model):
    """Application & finance data by law school, 2013"""

    __tablename__ = "schools"

    school_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    school_name = db.Column(db.String(50), nullable=False)
    applications = db.Column(db.Integer, nullable=False)
    admit_rate = db.Column(db.String(4), nullable=False)
    GPA_75 = db.Column(db.Float, nullable=False)
    GPA_50 = db.Column(db.Float, nullable=False)
    GPA_25 = db.Column(db.Float, nullable=False)
    LSAT_75 = db.Column(db.Integer, nullable=False)
    LSAT_50 = db.Column(db.Integer, nullable=False)
    LSAT_25 = db.Column(db.Integer, nullable=False)
    resident_tuition = db.Column(db.Float, nullable=False)
    nonresident_tuition = db.Column(db.Float, nullable=True)
    living_expense = db.Column(db.Float, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Application school_id=%s school_name=%s>" % (self.school_id, self.school_name)


class User(db.Model):
    """User id and GPA/LSAT score data"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(60), nullable=False)
    GPA = db.Column(db.Float, nullable=True)
    LSAT = db.Column(db.Float, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


# Helper functions


def connect_to_db(app):
    """Connect database to Flask app."""

    # Configure to use SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///law_school_info.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
