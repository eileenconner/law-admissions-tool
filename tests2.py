"""Test suite for Spot My School"""

import unittest
from server import app
from model import db, User, School, School_list
from model import generate_example_schools, generate_example_users, generate_example_school_lists


###############################
# TESTS FOR BASIC FUNCTIONALITY
###############################

class AppTestCase(unittest.TestCase):
    """Tests for app functionality when no user is in session."""

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

    ###################################
    # Tests for database entry creation

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

    def test_create_school_list(self):
        """test creating an item in School_list table"""
        school_list = School_list(user_id='1',
                                  school_id='1',
                                  admission_chance='Stretch',
                                  app_submitted='0')
        db.session.add(school_list)
        db.session.commit()

        self.assertEqual(school_list.user_id, 1)
        self.assertEqual(school_list.app_submitted, False)
        self.assertIsInstance(school_list, School_list)

        db.session.rollback()

    ###############################
    # Tests for html page rendering

    def test_index_page(self):
        """test that index page generates from template"""
        result = self.app.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Spot My School', result.data)

    def test_login_page(self):
        """test that login page generates from template"""

        result = self.app.get('/login')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Log in to find your law school matches', result.data)

    def test_register_page(self):
        """test that register page generates from template"""

        result = self.app.get('/register')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Register to find your law school matches', result.data)

    def test_profile_page(self):
        """test that profile page generates from template"""

        result = self.app.get('/profile')

        # currently no user in session, so redirects.
        self.assertEqual(result.status_code, 302)
        self.assertIn('text/html', result.headers['Content-Type'])

    def test_profile_page_redirects_to_login_if_no_user_logged_in(self):
        """test that profile page redirects to login page if no user logged in"""

        result = self.app.get('/profile', follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Log in to find your law school matches', result.data)

    def test_school_query_page(self):
        """test that school query page generates from template"""

        result = self.app.get('/school_query')

        # currently no user in session, so redirects.
        self.assertEqual(result.status_code, 302)
        self.assertIn('text/html', result.headers['Content-Type'])

    def test_school_query_page_redirects_to_login_if_no_user_logged_in(self):
        """test that school query page redirects to login page if no user logged in"""

        result = self.app.get('/school_query', follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Log in to find your law school matches', result.data)

    def test_if_page_does_not_exist_return_correct_status(self):
        """Test that attempting to load a page that doesn't exist returns 404 code."""
        result = self.app.get('/asdf')

        self.assertEqual(result.status_code, 404)
        self.assertIn('text/html', result.headers['Content-Type'])

    ############################
    # Tests for database queries

    def test_schools_alpha_list_page(self):
        """test that alphabetical school list page generates from template/db"""
        # add schools to db for testing purposes
        generate_example_schools()

        result = self.app.get('/schools')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Harvard', result.data)
        self.assertIn('Yale', result.data)

        db.session.rollback()

    def test_register_new_user(self):
        """Test that a new user registers correctly"""
        result = self.app.post('/register',
                               data={'email': 'jane@example.com',
                                     'password': 'password',
                                     'gpa': 3.2,
                                     'lsat': 160},
                               follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('You are now registered and may login.', result.data)

    def test_login_existing_user(self):
        """Test that an existing user can login"""
        # add example users
        generate_example_users()

        result = self.app.post('/login',
                               data={'email': 'jess@example.com',
                                     'password': 'password'},
                               follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('You have logged in.', result.data)

        db.session.rollback()

    def test_user_cannot_login_with_incorrect_password(self):
        """Test that a bad password will not let existing user log in"""
        # add example users
        generate_example_users()

        result = self.app.post('/login',
                               data={'email': 'jess@example.com',
                                     'password': 'wrong_password'},
                               follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Incorrect password.', result.data)

        db.session.rollback()

    def test_unknown_user_cannot_login(self):
        """Test that an unknown user cannot log in"""
        # add example users
        generate_example_users()

        result = self.app.post('/login',
                               data={'email': 'asdf@example.com',
                                     'password': 'password'},
                               follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('You are not registered as a user.', result.data)

        db.session.rollback()

    def test_existing_user_cannot_reregister(self):
        """Test that an existing user cannot reregister"""
        # add example users
        generate_example_users()

        result = self.app.post('/register',
                               data={'email': 'jane@example.com',
                                     'password': 'password',
                                     'gpa': 3.0,
                                     'lsat': 165},
                               follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('You are already registered.', result.data)

        db.session.rollback()


###########################
# TESTS FOR USER IN SESSION
###########################


class AppTestCaseSession(unittest.TestCase):
    """Tests for app functionality when user is in session."""

    def setUp(self):
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.app = app
        db.init_app(app)
        db.create_all()

        generate_example_schools()
        generate_example_users()
        generate_example_school_lists()

        # initiate session
        with self.app as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        # delete session here

    ##############################################
    # Tests for correct display given current user

    def test_index_page_displays_user_specific_options(self):
        """Test that index page displays correct options when user in session"""
        result = self.app.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Find my schools', result.data)

    def test_profile_page_displays_user_school_list(self):
        """Test that profile page displays user school list"""
        result = self.app.get('/profile')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('Your selected law schools', result.data)
        self.assertIn('Yale', result.data)

    def test_profile_page_displays_user_stats(self):
        """Test that profile page displays correct user stats"""
        result = self.app.get('/profile')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('3.2', result.data)
        self.assertIn('159', result.data)

    def test_school_query_displays_matches_for_logged_in_user(self):
        """Test that school query page displays appropriate schools for logged-in user"""
        result = self.app.get('/school_query')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('No matches found.', result.data)
        # determine which schools should come up -- need to mock out more data

    def test_school_query_displays_correctly_categorized_schools_for_logged_in_user(self):
        """Test that school query displays correctly categorized schools for logged-in user"""
        result = self.app.get('/school_query')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('No matches found.', result.data)
        # determine which schools should come up -- need to mock out more data

    def test_school_alpha_list_displays_add_buttons_when_user_logged_in(self):
        """Test that school list displays add buttons when user is logged in"""
        result = self.app.get('/schools')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('let user add school to their list', result.data)
        self.assertIn('assign admission chance based on categorization of school', result.data)

    ###########################
    # Tests to be implemented -- database changes while user is in session

    def test_add_schools_to_user_list(self):
        """Test that user can add schools to their list"""
        pass

    def test_remove_schools_from_user_list(self):
        """Test that user can remove schools from their list"""
        pass

    def test_user_can_change_gpa(self):
        """Test that user can change their GPA in the database"""
        pass

    def test_user_can_change_lsat(self):
        """Test that user can change their LSAT score in the database"""
        pass

    #################################
    # Tests to be implemented -- misc

    def test_logout(self):
        """Test that logout functionality works properly"""
        pass

##############
# Run unittest

if __name__ == '__main__':
    unittest.main()
