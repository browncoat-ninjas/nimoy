import unittest


class UnitTestExecutionFramework:
    def __init__(self, stream=None):
        self.suite = unittest.TestSuite()
        self.stream = stream

    def append_test(self, test):
        self.suite.addTest(test)

    def run(self):
        return unittest.TextTestRunner(stream=self.stream, verbosity=2).run(self.suite)
