import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config.config_environments['development'])
app.config['SECRET_KEY'] = "123bucketlistapp"

db = SQLAlchemy(app)
