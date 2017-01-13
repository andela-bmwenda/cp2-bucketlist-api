from flask import jsonify
from flask_restful import Resource
from app.models import db, User


class BucketList(Resource):

    def get(self):

        user = User("Bonny", 1234)

    def post(self):
        pass


class BucketListEntry(Resource):

    def get(self, bucketlist_id):
        return jsonify("something is here!")

    def put(self, bucketlist_id):
        pass

    def delete(self, bucketlist_id):
        pass
