from datetime import datetime

from flask import request, jsonify
from flask_restful import Resource

from app.auth import authenticate_token
from app.models import (db, BucketList, BucketlistItemSchema,
                        BucketlistSchema)


schema = BucketlistItemSchema()
bucketlist_schema = BucketlistSchema()


class BucketLists(Resource):
    """This class creates the endpoints
    for creating and getting bucketlists.
    """

    def get(self):
        """
        Gets all bucketlists
        """

        user = authenticate_token(request)
        limit = int(request.args.get("limit", 20))
        page = int(request.args.get("page", 1))
        if int(limit) > 100:
            limit = 100
        search = request.args.get('q', None)
        if search:
            bucketlists_query = BucketList.query.filter(
                BucketList.name.ilike('%' + search + '%')).filter_by(user_id=user.id)
            if not bucketlists_query.count():
                return {"message":
                        "No bucketlists found matching '{}'".format(search)}
        else:
            bucketlists_query = BucketList.query.filter_by(user_id=user.id)
        # Paginate bucketlist results
        bucketlists = bucketlists_query.paginate(page=page,
                                                 per_page=limit,
                                                 error_out=False)
        bucket_list = []
        for lst in bucketlists.items:
            items = lst.items.all()
            items_list = []
            for item in items:
                item_json = schema.dump(item)
                items_list.append(item_json.data)
            bucket_list.append({"id": lst.id,
                                "user_id": lst.user_id,
                                "name": lst.name,
                                "items": items_list,
                                "date_created": lst.date_created,
                                "date_modified": lst.date_modified,
                                "created_by": lst.created_by}
                               )
        return jsonify(bucket_list)

    def post(self):
        """Creates new bucketlist"""
        user = authenticate_token(request)
        data = request.get_json(silent=True)
        try:
            name = data["name"]
        except Exception:
            return {"error": "Bucketlist is missing 'name' parameter"}, 400
        exists = db.session.query(BucketList).filter_by(
            name=name).scalar() is not None
        if not exists:
            new_bucketlist = BucketList(name=name,
                                        user_id=user.id,
                                        created_by=user.username)
            db.session.add(new_bucketlist)
            db.session.commit()
            return {"message": "created new bucketlist",
                    "name": "{}".format(name)}, 201
        else:
            return {"message": "Bucketlist already exists"}


class BucketListSingle(Resource):
    """
    This class defines the endpoints
    for updating and deleting
    bucketlists
    """

    def get(self, bucketlist_id):
        """
        Gets a bucketlist with id <bucketlist_id>

        Returns the bucketlist as json
        """
        user = authenticate_token(request)
        bucketlist = BucketList.query.filter_by(
            id=bucketlist_id, user_id=user.id).first()
        if bucketlist:
            bucketlist_items = bucketlist.items.all()
            items_list = []
            for item in bucketlist_items:
                item_json = schema.dump(item)
                items_list.append(item_json.data)
            return jsonify({
                "name": bucketlist.name,
                "id": bucketlist.id,
                "items": items_list,
                "date_created": bucketlist.date_created,
                "date_modified": bucketlist.date_modified,
                "created_by": bucketlist.created_by
            })
        else:
            return {"error": "Bucketlist not found"}, 404

    def put(self, bucketlist_id):
        """Edits bucketlist with id <bucketlist_id>"""
        authenticate_token(request)
        bucketlist = self.get_bucketlist(bucketlist_id)
        if bucketlist:
            data = request.get_json(silent=True)
            new_name = data["name"]
            bucketlist.name = new_name
            bucketlist.date_modified = datetime.utcnow()
            db.session.add(bucketlist)
            db.session.commit()
            return {"message": "Modified bucketlist {0}".format(bucketlist.id)}
        else:
            return {"error": "Bucketlist not found"}, 404

    def delete(self, bucketlist_id):
        """Deletes bucketlist with id <bucketlist_id>"""
        authenticate_token(request)
        bucketlist = self.get_bucketlist(bucketlist_id)
        if bucketlist:
            db.session.delete(bucketlist)
            db.session.commit()
            return {"message": "Deleted bucketlist {0}"
                    .format(bucketlist_id)}, 204
        else:
            return {"error": "Bucketlist not found"}, 404

    def get_bucketlist(self, bucketlist_id):
        """Gets buckelist with the id <bucketlist_id>"""
        bucketlist = BucketList.query.get(bucketlist_id)
        if bucketlist:
            return bucketlist
        else:
            return None

    def not_found(self):
        """Error message for item not found"""
        return {"error": "Bucketlist not found"}, 404
