"""Models and database functions for law school application tool project."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


# Model definitions


class School(db.Model):
    """Application & finance data by law school, 2013"""

    __tablename__ = "schools"

    school_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    school_name = db.Column(db.String(50), nullable=False)
    applications = db.Column(db.Integer, nullable=False)
    admit_rate = db.Column(db.Float, nullable=False)
    gpa_75 = db.Column(db.Float, nullable=False)
    gpa_50 = db.Column(db.Float, nullable=False)
    gpa_25 = db.Column(db.Float, nullable=False)
    lsat_75 = db.Column(db.Integer, nullable=False)
    lsat_50 = db.Column(db.Integer, nullable=False)
    lsat_25 = db.Column(db.Integer, nullable=False)
    resident_tuition = db.Column(db.Integer, nullable=False)
    nonresident_tuition = db.Column(db.Integer, nullable=True)
    living_expense = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<School school_id=%s school_name=%s>" % (self.school_id, self.school_name)

    # Class methods for main user gpa/lsat match query
    @classmethod
    def id_safety_schools(cls, user_gpa, user_lsat):
        """Identify safety schools for logged-in user"""
        safety_schools = cls.query.filter(
            (user_gpa >= cls.gpa_75),
            (user_lsat >= cls.lsat_75)).order_by(cls.gpa_75.desc()).all()
        return safety_schools

    @classmethod
    def id_match_schools(cls, user_gpa, user_lsat):
        """Identify match schools for logged-in user"""
        match_schools = cls.query.filter(
            (user_gpa < cls.gpa_75),
            (user_gpa >= cls.gpa_50),
            (user_lsat < cls.lsat_75),
            (user_lsat >= cls.lsat_50)).order_by(cls.gpa_75.desc()).all()
        return match_schools

    @classmethod
    def id_stretch_schools(cls, user_gpa, user_lsat):
        """Identify stretch schools for logged-in user"""
        stretch_schools = cls.query.filter(
            (user_gpa < cls.gpa_50),
            (user_gpa >= cls.gpa_25),
            (user_lsat < cls.lsat_50),
            (user_lsat >= cls.lsat_25)).order_by(cls.gpa_50.desc()).all()
        return stretch_schools

    @classmethod
    def id_split_schools(cls, user_gpa, user_lsat):
        """Identify split schools for logged-in user"""
        split_schools = cls.query.filter(
            ((user_gpa >= cls.gpa_75) &
             (user_lsat <= cls.lsat_50)) |
            ((user_lsat >= cls.lsat_75) &
             (user_gpa <= cls.gpa_50))).order_by(cls.gpa_75.desc()).all()
        return split_schools

    # GPA-exclusive classmethods

    @classmethod
    def id_safety_schools_gpa(cls, user_gpa):
        """Identify safety schools for logged-in user by GPA only"""
        safety_schools = cls.query.filter(
            user_gpa >= cls.gpa_75).order_by(cls.gpa_75.desc()).all()
        return safety_schools

    @classmethod
    def id_match_schools_gpa(cls, user_gpa):
        """Identify match schools for logged-in user by GPA only"""
        match_schools = cls.query.filter(
            (user_gpa < cls.gpa_75),
            (user_gpa >= cls.gpa_50)).order_by(cls.gpa_75.desc()).all()
        return match_schools

    @classmethod
    def id_stretch_schools_gpa(cls, user_gpa):
        """Identify stretch schools for logged-in user by GPA only"""
        stretch_schools = cls.query.filter(
            (user_gpa < cls.gpa_50),
            (user_gpa >= cls.gpa_25)).order_by(cls.gpa_50.desc()).all()
        return stretch_schools

    # LSAT-exclusive classmethods
    @classmethod
    def id_safety_schools_lsat(cls, user_lsat):
        """Identify safety schools for logged-in user by LSAT score only"""
        safety_schools = cls.query.filter(
            user_lsat >= cls.lsat_75).order_by(cls.lsat_75.desc()).all()
        return safety_schools

    @classmethod
    def id_match_schools_lsat(cls, user_lsat):
        """Identify match schools for logged-in user by LSAT score only"""
        match_schools = cls.query.filter(
            (user_lsat < cls.lsat_75),
            (user_lsat >= cls.lsat_50)).order_by(cls.lsat_75.desc()).all()
        return match_schools

    @classmethod
    def id_stretch_schools_lsat(cls, user_lsat):
        """Identify stretch schools for logged-in user by LSAT score only"""
        stretch_schools = cls.query.filter(
            (user_lsat < cls.lsat_50),
            (user_lsat >= cls.lsat_25)).order_by(cls.lsat_50.desc()).all()
        return stretch_schools


class User(db.Model):
    """User id and GPA/LSAT score data"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)
    gpa = db.Column(db.Float, nullable=True)
    lsat = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class School_list(db.Model):
    """Items on user's target school list"""

    __tablename__ = "school_list"

    list_add_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey(School.school_id), nullable=False)
    admission_chance = db.Column(db.String(20), nullable=False)
    app_submitted = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='users')
    school = db.relationship('School', backref='schools')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<School_list list_add_id=%s>" % (self.list_add_id)


# Helper functions
def connect_to_db(app):
    """Connect database to Flask app."""

    # Configure to use SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///law_school_info.db'
    #app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # if we run this module interactively, you can work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
