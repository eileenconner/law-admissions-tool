"""Python unit tests for law school admission tool"""

import server
import unittest
# import doctest


# def load_tests(loader, tests, ignore):
#     """Also run doctests and file-based doctests."""

#     tests.addTests(doctest.DocTestSuite(server))
#     return tests


class SchoolTests(unittest.TestCase):
    """Tests for law school admission tool"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_testing_working(self):
        """Make sure this file is actually executing tests by raising a failure."""
        self.assertTrue(False)


class IntegrationTests(unittest.TestCase):
    """Tests Flask/html pieces for law school admission tool"""

    def setUp(self):
        # return test web browser w test_client()
        self.client = server.app.test_client()
        # include other things -- fake data, session user, fake db to test?

    def tearDown(self):
        # which one?
        # server.db.session.rollback()
        server.db.session.close()

    def test_homepage(self):
        result = server.test_client.get('/')
        self.assertEqual(result.status_code, 200)
        # self.assertIn('<h1>Test</h1>', result.data)


# run unit tests if running file in shell
if __name__ == "__main__":
    unittest.main()
