from datetime import datetime
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(50))

    def __init__(self, username, password):
        self.username = username
        self.password = password

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

    def __init__(self, name):
        self.name = name
        self.date_created = datetime.utcnow()
        self.date_modified = datetime.utcnow()
        self.created_by = None

    def __repr__(self):
        return '<BucketList %r>' % self.name


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

    def __init__(self, name):
        self.name = name
        self.date_created = datetime.utcnow()
        self.date_modified = datetime.utcnow()
        self.done = False

    def __repr__(self):
        return '<BucketListItem %r>' % self.name


# def test_db():
#     print("Here!")
#     user1 = User("Banks", 1234)
#     db.session.add(user1)
#     db.session.commit(user1)
#     b_list1 = BucketList("Kill a nigga")
#     user = User.query.filter_by(username="Banks").first()
#     b_list1.user_id = user.user_id
#     b_list1.created_by = user.username
#     db.session.add(b_list1)
#     db.session.commit(b_list1)


# if __name__ == '__main__':
#     test_db()