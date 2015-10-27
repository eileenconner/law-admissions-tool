"""Utility file to seed law school database from ABA data in seed_data/"""


"""
From aba-data-2013.txt

[0] SCHOOL
[1] Total Unduplicated Applications
[2] Total Unduplicated Offers (not using)
[3] Admit Rate
[4] 1L Matriculants (not using)
[5] 75th Percentile UGPA
[6] 50th Percentile UGPA
[7] 25th Percentile UGPA
[8] 75th Percentile LSAT
[9] 50th Percentile LSAT
[10] 25th Percentile LSAT
[11] Full-Time Resident Student Tuition
[12] Full-Time Non-Resident Student Tuition
[13] Single student living off-campus Living Expenses

Items separated by |
Can eliminate 2, 4 for unpacking purposes if desired

Additional desired info:
- school addresses
- school websites


"""

# import models from model.py
from model import School
from model import User
from model import connect_to_db, db
from server import app


def load_school_data():
    """Load school data to db from aba-data-2013.txt"""

    print "Schools"

    # Eliminate any previously seeded data
    School.query.delete()

    # For each row in file, split, strip, assign to row instance, and add to db
    for row in open("seed-data/aba-data-2013.txt"):
        row = row.split("|").rstrip()

        school_name = row[0]
        applications = row[1]
        admit_rate = row[3]
        gpa_75 = row[5]
        gpa_50 = row[6]
        gpa_25 = row[7]
        lsat_75 = row[8]
        lsat_50 = row[9]
        lsat_25 = row[10]
        resident_tuition = row[11]
        nonresident_tuition = row[12]
        living_expense = row[13]

        school_data = School(school_name=school_name,
                             applications=applications,
                             admit_rate=admit_rate,
                             gpa_75=gpa_75,
                             gpa_50=gpa_50,
                             gpa_25=gpa_25,
                             lsat_75=lsat_75,
                             lsat_50=lsat_50,
                             lsat_25=lsat_25,
                             resident_tuition=resident_tuition,
                             nonresident_tuition=nonresident_tuition,
                             living_expense=living_expense
                             )
        db.session.add(school_data)

    # commit all new adds to db
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # create all tables
    db.create_all()

    # Import school data into database
    load_school_data()

    # seeding confirmation
    print "It's done!"
