"""Python unit tests for law school admissions tool"""

import server
import unittest
import doctest


def load_tests(loader, tests, ignore):
    """Also run our doctests and file-based doctests."""

    tests.addTests(doctest.DocTestSuite(server))
    return tests


class SchoolTests(unittest.TestCase):
    """Tests for law school admission tool"""

    def test_user_stat_result(self):
        # insert something useful here
        #self.assertEqual(len(server.find_user_gpa_lsat()), 2)


# run unit tests if running file in shell
if __name__ == "__main__":
    unittest.main()
