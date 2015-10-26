"""Models and database functions for law school admissions tool project."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


# Model definitions


class Application(db.Model):
    """Application data by law school, 2013"""

    __tablename__ = "apps"

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

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Application school_id=%s school_name=%s>" % (self.school_id, self.school_name)


class Expense(db.Model):
    """Tuition and living expense data by law school, 2013"""

    __tablename__ = "expenses"

    school_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    school_name = db.Column(db.String(50), nullable=False)
    resident_tuition = db.Column(db.Float, nullable=False)
    nonresident_tuition = db.Column(db.Float, nullable=True)
    living_expense = db.Column(db.Float, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Expense school_id=%s school_name=%s>" % (self.school_id, self.school_name)


# class School(db.Model):
#     """Law school basic info: address, website"""
#     # No current source for this info, but ideally I'd like to add it.

#     __tablename__ = "schools"

#     school_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     address = db.Column(db.String, nullable=False)
#     website = db.Column(db.String, nullable=False)

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<School school_id=%s address=%s>" % (self.school_id, self.address)


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
