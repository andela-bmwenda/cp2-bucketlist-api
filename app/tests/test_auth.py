from . base_test_case import BaseTestCase
import json


class AuthTestCase(BaseTestCase):

    def test_registration_with_invalid_format(self):
        data = json.dumps({"username": "Hugo",
                           "password": 1234,
                           "invalid": "Invalid entry"}
                          )
        response = self.client.post('/auth/register',
                                    data=data,
                                    content_type='application/json',
                                    headers={}
                                    )
        self.assertEqual(response.json["error"],
                         "Invalid format. " +
                         "Only username and Password are allowed")

    def test_registration_with_no_data(self):
        response = self.client.post('/auth/register',
                                    data=json.dumps({}),
                                    content_type='application/json',
                                    headers={}
                                    )
        self.assertEqual(response.json["error"],
                         "Please enter registration data")

    def test_registration_with_missing_data(self):
        data = json.dumps({"username": "Tester"})
        response = self.client.post('/auth/register',
                                    data=data,
                                    content_type='application/json',
                                    headers={}
                                    )
        self.assertEqual(response.json["error"],
                         "username or password is missing")

    def test_registration_with_existing_username(self):
        data = json.dumps({"username": "Tester",
                           "password": "password"})
        response = self.client.post('/auth/register',
                                    data=data,
                                    content_type='application/json',
                                    headers={}
                                    )
        self.assertEqual(response.json["message"], "Tester already exists")

    def test_registration_works(self):
        data = json.dumps({"username": "Hugo",
                           "password": 1234})
        response = self.client.post('/auth/register',
                                    data=data,
                                    content_type='application/json',
                                    headers={}
                                    )
        self.assertEqual(response.json["message"],
                         "Successfully registered Hugo")

    def test_login_with_invalid_password(self):
        data = json.dumps({"username": "Tester",
                           "password": "wrong"})
        response = self.client.post('/auth/login',
                                    data=data,
                                    content_type='application/json',
                                    headers={}
                                    )
        self.assertEqual(response.json["error"], "Invalid password")

    def test_login_with_missing_data(self):
        data = json.dumps({"username": "Tester"})
        response = self.client.post('/auth/login',
                                    data=data,
                                    content_type='application/json',
                                    headers={}
                                    )
        self.assertEqual(response.json["error"],
                         "username or password is missing")

    def test_login_with_no_data(self):
        response = self.client.post('/auth/login',
                                    content_type='application/json',
                                    headers={}
                                    )
        self.assertEqual(response.json["error"],
                         "Login data not found")

    def test_login_works(self):
        data = json.dumps({"username": "Tester",
                           "password": "password"
                           })
        response = self.client.post('/auth/login',
                                    data=data,
                                    content_type='application/json',
                                    headers={}
                                    )
        self.assertEqual(response.json["message"], "Login successful")
