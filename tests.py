"""Python unit tests for law school admission tool"""

import unittest

from server import app
from model import db
from model import User


class SchoolTests(unittest.TestCase):
    """Tests for law school admission tool"""

    def setUp(self):
        """Set up database for testing purposes"""
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.app = app
        db.init_app(app)
        db.create_all()
        print "setup ran"

    def tearDown(self):
        """Remove testing db"""
        db.session.remove()
        db.drop_all()
        print "teardown ran"

    # def test_testing_working(self):
    #     """Make sure this file is actually executing tests by raising a failure."""
    #     self.assertTrue(False)

    def test_user_creation(self):
        """Test creating a user in db"""
        user = User(email='test@test.com', password='password', gpa='3.5', lsat='160')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.email, 'test@test.com')
        db.session.rollback()


    # help/examples
    # “self.client.post(“/my-route”, {‘fieldone’: ‘blah’, ‘fieldtwo’: ‘blah’})”
    # s = Student.query.filter(id == new_student.id).one(); self.assertEqual(s.grade, ‘A’)


# class IntegrationTests(unittest.TestCase):
#     """Tests Flask/html pieces for law school admission tool"""

#     def test_homepage(self):
#         result = server.test_client.get('/')
#         self.assertEqual(result.status_code, 200)
#         # self.assertIn('<h1>Test</h1>', result.data)


# run unit tests if running file in shell
if __name__ == "__main__":
    unittest.main()
