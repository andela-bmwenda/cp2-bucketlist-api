from . base_test_case import BaseTestCase
import json


class AuthTestCase(BaseTestCase):

    def setUp(self):

        self.credentials = json.dumps({"username": "Hugo",
                                      "password": 1234})

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
        self.assertEqual(response.json,
                         "Registration should only contain username and password")

    def test_registration_with_existing_username(self):

        self.client.post('/auth/register',
                         data=self.credentials,
                         content_type='application/json',
                         headers={}
                         )
        response = self.client.post('/auth/register',
                                    data=self.credentials,
                                    content_type='application/json',
                                    headers={}
                                    )
        self.assertEqual(response.json, "User already exists")

    def test_registration_works(self):

        response = self.client.post('/auth/register',
                                    data=self.credentials,
                                    content_type='application/json',
                                    headers={}
                                    )
        self.assertEqual(response.json, "Registration successful")

    def test_login_with_invalid_credentials(self):

        login_data = json.dumps({"username": "Hugo",
                                 "password": "invalid"
                                 })
        self.client.post('/auth/register',
                         data=self.credentials,
                         content_type='application/json',
                         headers={}
                         )
        response = self.client.post('/auth/login',
                                    data=login_data,
                                    content_type='application/json',
                                    headers={}
                                    )
        self.assertEqual(response.json, "Invalid credentials")

    def test_login_works(self):

        registration_data = json.dumps({"username": "Hugo",
                                        "password": 1234
                                        })
        login_data = json.dumps({"username": "Hugo",
                                 "password": 1234
                                 })
        self.client.post('/auth/register',
                         data=registration_data,
                         content_type='application/json',
                         headers={}
                         )
        response = self.client.post('/auth/login',
                                    data=login_data,
                                    content_type='application/json',
                                    headers={}
                                    )
        self.assertEqual(response.json, "Login successful")

    def test_it_requires_token(self):
        pass

    def test_for_invalid_token(self):
        pass

    def test_for_expired_token(self):
        pass
