from . base_test_case import BaseTestCase
import json


class BucketListApiTestCase(BaseTestCase):

    def setUp(self):
        self.bucketlist = json.dumps({"name": "some bucketlist",
                                      "created_by": "me",
                                      })

    def post(self):

        response = self.client.post('/bucketlists',
                                    data=self.bucketlist,
                                    content_type='application/json',
                                    headers={}
                                    )
        return response

    # Tests for entire bucketlist
    def test_cannot_create_empty_bucketlist(self):

        response = self.client.post('/bucketlists',
                                    data=json.dumps({}),
                                    content_type='application/json',
                                    headers={}
                                    )
        self.assertEqual(response.json, "Error! Bucketlist has no data")

    def test_return_message_if_no_bucketlists_exist(self):

        response = self.client.get('/bucketlists',
                                   content_type='application/json',
                                   headers={}
                                   )
        self.assertEqual(response.json, "No bucketlists to display")

    def test_cannot_create_duplicate_bucketlist(self):

        self.post()
        self.assertEqual(self.post().json, "Bucketlist already exists")

    def test_it_gets_all_bucket_lists(self):

        self.post()
        response = self.client.get('/bucketlists',
                                   content_type='application/json',
                                   headers={}
                                   )
        self.assertEqual(response.json, 200)
        self.assertIn("name", response.json)

    def test_it_creates_new_bucket_list(self):

        response = self.post()
        self.assertEqual(response.status_code, 201)
        # Assert that an item was added to db

    # Tests for single bucketlist entry
    def test_cannot_get_non_existent_bucketlist(self):

        self.post()
        response = self.client.get('/bucketlists/11',
                                   content_type='application/json',
                                   headers={}
                                   )
        self.assertEqual(response.json, "Bucketlist does not exist")

    def test_it_gets_bucketlist(self):

        self.post()
        response = self.client.get('/bucketlists/1',
                                   content_type='application/json',
                                   headers={}
                                   )
        self.assertIn("name", response.json)

    def test_cannot_update_non_existent_bucketlist(self):

        data = json.dumps({"new name": "something else"})
        self.post()
        response = self.client.put('/bucketlists/11',
                                   data=data,
                                   content_type='application/json',
                                   headers={}
                                   )
        self.assertEqual(response.json, "Item does not exist")

    def test_it_updates_bucketlist(self):

        data = json.dumps({"new name": "something else"})
        self.post()
        response = self.client.put('/bucketlists/1',
                                   data=data,
                                   content_type='application/json',
                                   headers={}
                                   )
        self.assertEqual(response.status_code, 200)

    def test_cannot_delete_non_existent_bucketlist(self):

        self.post()
        response = self.client.delete('/bucketlists/11',
                                      content_type='application/json',
                                      headers={}
                                      )
        self.assertEqual(response.json, "Item does not exist")

    def test_it_deletes_bucketlist(self):

        self.post()
        response = self.client.delete('/bucketlists/1',
                                      content_type='application/json',
                                      headers={}
                                      )
        self.assertEqual(response.status_code, 200)
        # Assert that an item was delted from db
