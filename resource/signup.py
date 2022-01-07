import bcrypt
from app import db
from model.account import Account
from model.post import Post
from model.comment import Comment
from model.post import Post
from flask_restful import Resource, marshal, reqparse, fields, marshal_with

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, help='Username login to system')
parser.add_argument('password', type=str, help='Password login to system')
parser.add_argument('is_active', type=bool, help='Active of account')

resource_fields = {
    'username': fields.String,
    'is_active': fields.Boolean,
    'created_at': fields.DateTime(dt_format='rfc822'),
}

class SignupResource(Resource):

    # Api create account
    def post(self):
        # Receive data from request
        args = parser.parse_args()
        # Check user exists
        account = Account.query.filter_by(username=args["username"]).first()
        if account:
            return {
            "statusCode": 400,
            "message": "Account existed!"
        }, 400
        # Create new account for system
        # hash password
        password = bcrypt.hashpw(str.encode(args["password"], encoding='UTF-8'), bcrypt.gensalt())
        account = Account(
            username=args["username"], password=password.decode('UTF-8')
        )
        db.session.add(account)
        db.session.commit()
        return {
            "statusCode": 200,
            "message": "Create new account success!"
        }, 200
            