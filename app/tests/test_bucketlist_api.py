from . base_test_case import BaseTestCase
import json


class BucketListApiTestCase(BaseTestCase):

    def post(self, payload):
        response = self.client.post('/bucketlists',
                                    data=json.dumps(payload),
                                    content_type='application/json',
                                    headers={"Authorization": self.token}
                                    )
        return response

    # Tests for entire bucketlist
    def test_create_empty_bucketlist(self):

        response = self.post({})
        self.assertEqual(response.json,
                         {"error": "Bucketlist is missing 'name' parameter"})

    def test_create_new_bucket_list(self):
        response = self.post({"name": "New bucketlist"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {
                             "message": "created new bucketlist",
                             "name": "New bucketlist"
                         })

    def test_create_duplicate_bucketlist(self):
        self.post({"name": "Test bucketlist"})
        response = self.post({"name": "Test bucketlist"})
        self.assertEqual(
            response.json, {"message": "Bucketlist already exists"})

    def test_get_all_bucket_lists(self):
        self.post({"name": "Bucketlist one"})
        self.post({"name": "Bucketlist two"})
        self.post({"name": "Bucketlist three"})
        response = self.client.get('/bucketlists',
                                   content_type='application/json',
                                   headers={"Authorization": self.token}
                                   )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 4)

    # Tests for single bucketlist entry
    def test_get_non_existent_bucketlist(self):
        # self.post({"name": "Test bucketlist"})
        response = self.client.get('/bucketlists/11',
                                   content_type='application/json',
                                   headers={"Authorization": self.token}
                                   )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json,
                         {"error": "Bucketlist not found"})

    def test_get_bucketlist(self):
        response = self.client.get('/bucketlists/1',
                                   content_type='application/json',
                                   headers={"Authorization": self.token}
                                   )
        self.assertEqual(response.json["name"],
                         "Test bucketlist")

    def test_update_non_existent_bucketlist(self):
        payload = {"new name": "something else"}
        response = self.client.put('/bucketlists/11',
                                   data=payload,
                                   content_type='application/json',
                                   headers={"Authorization": self.token}
                                   )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json,
                         {"error": "Bucketlist not found"})

    def test_update_bucketlist(self):
        payload = json.dumps({"name": "Renamed bucketlist"})
        self.post({"name": "Test bucketlist"})
        response = self.client.put('/bucketlists/1',
                                   data=payload,
                                   content_type='application/json',
                                   headers={"Authorization": self.token}
                                   )
        self.assertEqual(response.status_code, 200)

    def test_delete_non_existent_bucketlist(self):
        response = self.client.delete('/bucketlists/11',
                                      content_type='application/json',
                                      headers={"Authorization": self.token}
                                      )
        self.assertEqual(response.status_code, 404)

    def test_delete_bucketlist(self):
        self.post({"name": "Test bucketlist"})
        response = self.client.delete('/bucketlists/1',
                                      content_type='application/json',
                                      headers={"Authorization": self.token}
                                      )
        self.assertEqual(response.status_code, 204)
