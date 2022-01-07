import datetime
import bcrypt
import jwt
from app import app
from model.account import Account
from flask_restful import Resource, marshal, reqparse, fields, marshal_with

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, help='Username login to system')
parser.add_argument('password', type=str, help='Password login to system')

resource_fields = {
    'token': fields.String
}

class LoginResource(Resource):

    # Api create account
    def post(self):
        # Receive data from request
        args = parser.parse_args()
        # Check user exists
        account = Account.query.filter_by(username=args["username"]).first()
        if not account:
            return {
            "statusCode": 400,
            "message": "Account not existed!"
        }, 400
        # verify password
        if bcrypt.checkpw(args["password"].encode('utf-8'), account.password.encode('utf-8')):
            # generates the JWT Token
            token = jwt.encode({
                'id': account.id,
                'exp' : datetime.datetime.now() + datetime.timedelta(minutes = 30)
            }, app.config['SECRET_KEY'], 'HS256')
            return {
                "statusCode": 200,
                "message": "login success!",
                "token": token
            }, 201
        return {
                "statusCode": 400,
                "message": "Password not mapping!",
        }, 400
