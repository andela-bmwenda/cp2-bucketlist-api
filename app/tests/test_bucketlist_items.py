from . base_test_case import BaseTestCase
import json


class BucketListItemsTestCase(BaseTestCase):

    def post(self, payload):
        response = self.client.post('/bucketlists/1/items',
                                    data=json.dumps(payload),
                                    content_type='application/json',
                                    headers={"Authorization": self.token}
                                    )
        return response

    # Tests for all items in a bucketlist
    def test_create_empty_buckelist_item(self):
        response = self.post({})
        self.assertEqual(response.json,
                         {"error": "Item is missing 'name' parameter"})

    def test_create_duplicate_item(self):
        response = self.post({"name": "Test item"})
        self.assertEqual(response.json,
                         {"error": "Item already exists"})

    def test_create_bucketlist_item(self):
        response = self.post({"name": "New item"})
        self.assertEqual(response.json,
                         {"message": "created new item",
                          "name": "New item"})

    def test_get_bucketlist_items(self):
        self.post({"name": "Item one"})
        self.post({"name": "Item two"})
        self.post({"name": "Item three"})
        response = self.client.get('/bucketlists/1/items',
                                   content_type='application/json',
                                   headers={"Authorization": self.token}
                                   )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 4)

    # Tests for single item in bucketlist
    def test_get_non_existent_item(self):
        response = self.client.get('/bucketlists/1/items/11',
                                   content_type='application/json',
                                   headers={"Authorization": self.token}
                                   )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json,
                         {"error": "Item not found"})

    def test_get_bucketlist_item(self):
        response = self.client.get('/bucketlists/1/items/1',
                                   content_type='application/json',
                                   headers={"Authorization": self.token}
                                   )
        self.assertIn("Test item", response.json["name"])

    def test_update_non_existent_item(self):
        data = {"name": "new name", "done": True}
        response = self.client.put('/bucketlists/1/items/2',
                                   data=json.dumps(data),
                                   content_type='application/json',
                                   headers={"Authorization": self.token}
                                   )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json,
                         {"error": "Item not found"})

    def test_delete_non_existent_item(self):
        response = self.client.delete('/bucketlists/1/items/',
                                      content_type='application/json',
                                      headers={"Authorization": self.token}
                                      )
        self.assertEqual(response.status_code, 404)

    def test_update_bucketlist_item(self):
        data = json.dumps({"name": "new name", "done": True})
        response = self.client.put('/bucketlists/1/items/1',
                                   data=data,
                                   content_type='application/json',
                                   headers={"Authorization": self.token}
                                   )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Modified item 1"})

    def test_delete_bucketlist_item(self):
        self.post({"name": "kill me"})
        response = self.client.delete('/bucketlists/1/items/1',
                                      content_type='application/json',
                                      headers={"Authorization": self.token}
                                      )
        self.assertEqual(response.status_code, 204)
