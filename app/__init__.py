from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/v1/api/*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'secret'
app.config["ALLOWED_EXTENSIONS"] = set(['png', 'jpg', 'jpeg'])
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@localhost/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

api = Api(app)

from app import routes