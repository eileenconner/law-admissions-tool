"""Python unit tests for law school admissions tool"""

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
        # return test web browser w test_client()
        self.client = server.app.test_client()

    def tearDown(self):
        pass
        # which one?
        server.db.session.rollback()
        server.db.session.close()

    def test_testing_working(self):
        """Make sure this file is actually executing tests by raising a failure."""
        self.assertTrue(False)


# run unit tests if running file in shell
if __name__ == "__main__":
    unittest.main()
