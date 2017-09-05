import unittest


def create_suite():
    return unittest.TestSuite()


def append_test(suite, test):
    suite.addTest(test)


def run(suite):
    return unittest.TextTestRunner(verbosity=2).run(suite)
