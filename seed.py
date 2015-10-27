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
        row = row.rstrip().split("|")

        school_name = row[0].rstrip().title()
        applications = row[1].rstrip()
        admit_rate = row[3].rstrip()
        gpa_75 = row[5].rstrip()
        gpa_50 = row[6].rstrip()
        gpa_25 = row[7].rstrip()
        lsat_75 = row[8].rstrip()
        lsat_50 = row[9].rstrip()
        lsat_25 = row[10].rstrip()
        resident_tuition = row[11].rstrip()
        nonresident_tuition = row[12].rstrip()
        living_expense = row[13].rstrip()

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
        print school_data

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
