import unittest
from server import app
from model import db, User, School
# from model import School_list


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.app = app
        db.init_app(app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        """test creating an item in User table"""
        user = User(email='jim@example.com', password='password', gpa='3.2', lsat='159')
        db.session.add(user)
        db.session.commit()

        self.assertEqual(user.email, 'jim@example.com')
        self.assertEqual(user.password, 'password')
        self.assertEqual(user.gpa, 3.2)
        self.assertEqual(user.lsat, 159)
        self.assertIsInstance(user, User)

        db.session.rollback()

    def test_create_school(self):
        """test creating an item in School table"""
        school = School(school_name='Harvard',
                        applications='1000',
                        admit_rate='.3',
                        gpa_75='4.0',
                        gpa_50='3.8',
                        gpa_25='3.6',
                        lsat_75='180',
                        lsat_50='175',
                        lsat_25='170',
                        resident_tuition='50000',
                        nonresident_tuition='50000',
                        living_expense='20000',
                        url='www.harvard.edu',
                        address='Boston, MA',
                        latitude='00.0000',
                        longitude='00.0000')
        db.session.add(school)
        db.session.commit()

        self.assertEqual(school.school_name, 'Harvard')
        self.assertEqual(school.admit_rate, .3)
        self.assertIsInstance(school, School)

        db.session.rollback()

    # def test_create_school_list(self):
    #     """test creating an item in School_list table"""
    #     # do we need to create user/school for this to work, since those ids are foreign keys?
    #     school_list = School_list(user_id='1',
    #                               school_id='1',
    #                               admission_chance='Stretch',
    #                               app_submitted='False')
    #     db.session.add(school_list)
    #     db.session.commit()

    #     self.assertEqual(school_list.user_id, 1)
    #     self.assertEqual(school_list.app_submitted, 'False')
    #     self.assertIsInstance(school_list, School_list)

    #     db.session.rollback()


if __name__ == '__main__':
    unittest.main()
