from datetime import datetime, timedelta
import jwt

from flask_testing import TestCase

from app.models import User, BucketList, BucketListItem
from config import Config, config_environments
from manage import app, db


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object(config_environments['testing'])
        return app

    def setUp(self):
        self.client = self.app.test_client()
        db.drop_all()
        db.create_all()

        # Add a test user to test db
        user = User("Tester", "password")
        db.session.add(user)
        db.session.commit()

        # Generate token
        payload = {"sub": user.id,
                   "exp": datetime.utcnow() + timedelta(minutes=5)
                   }
        encoded_token = jwt.encode(
            payload, Config.SECRET_KEY, algorithm='HS256')
        self.token = encoded_token.decode('utf-8')

        # Add a bucketlist to test db
        user = User.query.filter_by(username="Tester").first()
        bucketlist = BucketList("Test bucketlist", user.id, user.username)
        db.session.add(bucketlist)
        db.session.commit()

        # Add a bucketlist item to test db
        bucketlist = BucketList.query.filter_by(name="Test bucketlist").first()
        bucketlist_item = BucketListItem("Test item", bucketlist.id)
        db.session.add(bucketlist_item)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
