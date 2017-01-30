from datetime import datetime

from flask_login import UserMixin
from marshmallow import Schema, fields
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(50))

    def __init__(self, username, password):
        self.username = username
        self.set_password(password=bytes(str(password), 'utf-8'))
        self.password = self.pwd_hash

    def set_password(self, password):
        self.pwd_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username


class BucketList(db.Model):
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship('User',
                           backref=db.backref('bucketlists', lazy='dynamic'))
    name = db.Column(db.String(100))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    created_by = db.Column(db.String(20))

    def __init__(self, name, user_id, created_by):
        self.name = name
        self.user_id = user_id
        self.created_by = created_by
        self.date_created = datetime.utcnow()
        self.date_modified = datetime.utcnow()

    def __repr__(self):
        return '<BucketList %r>' % self.name


class BucketlistSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
    created_by = fields.Str()


class BucketListItem(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(BucketList.id))
    bucketlist = db.relationship('BucketList',
                                 backref=db.backref('items', lazy='dynamic'))
    name = db.Column(db.String(100))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, name, bucketlist_id):
        self.name = name
        self.bucketlist_id = bucketlist_id
        self.date_created = datetime.utcnow()
        self.date_modified = datetime.utcnow()
        self.done = False

    def __repr__(self):
        return '<BucketListItem %r>' % self.name


class BucketlistItemSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
    done = fields.Bool()
