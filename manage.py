from flask_restful import Api
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import app, db
from app.auth import Register, Login
from app.bucketlist_api import BucketLists, BucketListSingle
from app.bucketlist_items import BucketListItems, BucketListItemSingle

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

api = Api(app)

api.add_resource(Register, '/auth/register')
api.add_resource(Login, '/auth/login')
api.add_resource(BucketLists, '/bucketlists')
api.add_resource(BucketListSingle, '/bucketlists/<int:bucketlist_id>')
api.add_resource(BucketListItems, '/bucketlists/<int:bucketlist_id>/items')
api.add_resource(BucketListItemSingle,
                 '/bucketlists/<int:bucketlist_id>/items/<int:item_id>')

if __name__ == '__main__':
    manager.run()
