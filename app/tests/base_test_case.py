from flask_testing import TestCase
from config import config_environments
from manage import app


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object(config_environments['testing'])
        return app

    def setUp(self):
        self.client = self.create_app().test_client()

    def tearDown(self):
        pass
