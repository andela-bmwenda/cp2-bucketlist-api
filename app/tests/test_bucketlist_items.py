from . base_test_case import BaseTestCase
import json


class BucketListItemsTestCase(BaseTestCase):

    def setUp(self):

        self.item = json.dumps({"name": "some bucketlist",
                                "done": False
                                })

    def post(self):

        response = self.client.post('/bucketlists/1/items',
                                    data=self.item,
                                    content_type='application/json',
                                    headers={}
                                    )
        return response

    # Tests for all items in a bucketlist
    def test_cannot_create_empty_buckelist_item(self):

        response = self.client.post('/bucketlists/1/items',
                                    data=json.dumps({}),
                                    content_type='application/json',
                                    headers={}
                                    )
        self.assertEqual(response.json, "Error! Bucketlist item has no data")

    def test_cannot_create_duplicate_item(self):

        self.post()
        self.assertEqual(self.post().json, "Bucketlist item already exists")

    def test_it_creates_bucketlist_item(self):

        self.assertEqual(self.post().json, self.item)
        # Assert that an item was added to db

    def test_it_gets_bucketlist_items(self):

        self.post()
        response = self.client.get('/bucketlists/1/items',
                                   content_type='application/json',
                                   headers={}
                                   )
        self.assertEqual(response.status_code, 201)

    # Tests for single item in bucketlist
    def test_cannot_get_non_existent_item(self):

        response = self.client.get('/bucketlists/1/items/1',
                                   data=self.item,
                                   content_type='application/json',
                                   headers={}
                                   )
        self.assertEqual(response.json,
                         "Bucket list item does not exist")

    def test_it_gets_bucketlist_item(self):

        self.post()
        response = self.client.get('/bucketlists/1/items/1',
                                   data=self.item,
                                   content_type='application/json',
                                   headers={}
                                   )
        self.assertEqual(response.json, self.item)

    def test_cannot_update_non_existent_item(self):

        response = self.client.put('/bucketlists/1/items/1',
                                   data=self.item,
                                   content_type='application/json',
                                   headers={}
                                   )
        self.assertEqual(response.json, "Bucketlist item does not exist")

    def test_cannot_delete_non_existent_item(self):

        response = self.client.delete('/bucketlists/1/items/1',
                                      data=self.item,
                                      content_type='application/json',
                                      headers={}
                                      )
        self.assertEqual(response.json, "Bucketlist item does not exist")

    def test_it_updates_bucketlist_item(self):

        data = json.dumps({"name": "Modified something"})
        self.post()
        response = self.client.put('/bucketlists/1/items/1',
                                   data=data,
                                   content_type='application/json',
                                   headers={}
                                   )
        self.assertEqual(response.status_code, 201)

    def test_it_deletes_bucketlist_item(self):

        self.post()
        response = self.client.delete('/bucketlists/1/items/1',
                                      content_type='application/json',
                                      headers={}
                                      )
        self.assertEqual(response.json, 204)
        # Assert that an item was delted from db

