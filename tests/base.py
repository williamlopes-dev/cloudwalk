import unittest

from fraud_prevention.app import app

class Base(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config.update({
            "TESTING": True,
        })
        self.client = self.app.test_client()
        self.app.extensions['limiter'].reset()

    def tearDown(self):
        pass
