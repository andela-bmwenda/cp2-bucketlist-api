from datetime import datetime, timedelta

from flask import jsonify, request
from flask_restful import abort, Resource
import jwt

from app.models import db, User
from config import Config


def authenticate_token(request):
    """
    Checks that a token is present and valid
    Returns user instance.
    """
    token = request.headers.get("Authorization")
    if not token:
        abort(401, message="No authorized token")
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithm="HS256")
    except jwt.DecodeError:
        abort(401, message="Invalid token")
    except jwt.ExpiredSignatureError:
        abort(401, message="Session expired, please login again")
    user = User.query.get(int(payload['sub']))
    return user


class Register(Resource):
    """
    This class creates end points for registering users.
    """

    def post(self):
        """Endpoint for registering users"""
        data = request.get_json(silent=True)
        if not data:
            return {"error": "Please enter registration data"}, 400
        elif len(data) > 2:
            return {"error": "Invalid format. " +
                    "Only username and Password are allowed"}, 400
        try:
            username = data["username"]
            password = data["password"]
        except Exception:
            return {"error": "username or password is missing"}, 400
        user = User.query.filter_by(username=username).first()
        if user:
            return {"message": "{} already exists".format(user.username)}, 400
        else:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            return {"message": "Successfully registered {0}".format(username)}


class Login(Resource):
    """Class that creates endpoints for login"""

    def post(self):
        """End point for login"""
        data = request.get_json(silent=True)
        if not data:
            return {"error": "Login data not found"}, 400
        try:
            username = data["username"]
            password = data["password"]
        except Exception:
            return {"error": "username or password is missing"}, 400
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"error": "{0} is not registered".format(username)}, 400
        elif user and not user.check_password(password=bytes(str(password), 'utf-8')):
            return {"error": "Invalid password"}, 403
        else:
            payload = {"sub": user.id,
                       "exp": datetime.utcnow() + timedelta(minutes=30)
                       }
            token = jwt.encode(
                payload, Config.SECRET_KEY, algorithm='HS256')
            return jsonify({"message": "Login successful",
                            "token": token.decode('utf-8'),
                            })
