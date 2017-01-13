from flask import jsonify
from flask_restful import Resource


class BucketListItems(Resource):

    def post(self, bucketlist_id):
        return jsonify("Bucketlist {} has a new item!".format(bucketlist_id))

    def get(self, bucketlist_id):
        pass


class BucketListItemSingle(Resource):

    def get(self, bucketlist_id, item_id):
        pass

    def put(self, bucketlist_id, item_id):
        pass

    def delete(self, bucketlist_id, item_id):
        pass
