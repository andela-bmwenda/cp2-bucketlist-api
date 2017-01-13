from time import time
from flask import jsonify
from flask_restful import Api, Resource
import jwt
from app import app

api = Api(app)


class Register(Resource):

    def post(self):
        pass


class Login(Resource):

    def post(self):
        pass


if __name__ == '__main__':
    app.run(debug=True)
