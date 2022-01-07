import bcrypt
from app import db
from app.jwt import token_required
from model.account import Account
from flask_restful import Resource, reqparse, fields

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, help='Username login to system')
parser.add_argument('password', type=str, help='Password login to system')
parser.add_argument('is_active', type=bool, help='Active of account')

resource_fields = {
    'username': fields.String,
    'is_active': fields.Boolean,
    'created_at': fields.DateTime(dt_format='rfc822'),
}

class UserListResource(Resource):
    # Api get all account
    @token_required
    def get(self, current_user, *args, **kwargs):
        # check current account is admin or not
        if current_user.is_admin:
            users = Account.query.filter(~Account.id.in_([current_user.id]))
        else:
            users = Account.query.filter_by(id=current_user.id)
        data_resposne = [{
            "id": item.id,
            "username": item.username,
            "is_admin": item.is_admin,
            "is_active": item.is_active,
            "created_at": item.created_at.strftime("%Y-%m-%d")
            
        } for item in users]
        return {
            "statusCode": 200,
            "message": "Get all users",
            "results": data_resposne
        }, 200


class UserResource(Resource):

    # Api get detail user
    @token_required
    def get(self, current_user, *args, **kwargs):
        # check current account is admin or not
        item = Account.query.filter_by(id=kwargs["account_id"]).first()
        if not item:
            return {
            "statusCode": 400,
            "message": "Account not exists!"
        }, 400
        data_resposne = {
            "id": item.id,
            "username": item.username,
            "is_admin": item.is_admin,
            "is_active": item.is_active,
            "created_at": item.created_at.strftime("%Y-%m-%d")
            
        }
        return {
            "statusCode": 200,
            "message": "Get detail user",
            "results": data_resposne
        }, 200

    # Api create account
    @token_required
    def post(self, current_user, *args, **kwargs):
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

    @token_required
    def delete(self,current_user, *args, **kwargs):
        # Start a sesssion transaction
        # Get account for delete
        account = Account.query.filter_by(id=kwargs["account_id"]).first()
        if not account:
            return {
            "statusCode": 400,
            "message": "Account not exists!"
        }, 400
        db.session.delete(account)
        db.session.commit()
        return {
            "statusCode": 204,
            "message": "Delete account success!"
        }, 200

    @token_required
    def put(self,current_user, *args, **kwargs):
        # Receive data from request
        args = parser.parse_args()
        account: Account = Account.query.filter_by(id=kwargs["account_id"]).first()
        if not account:
            return {
            "statusCode": 400,
            "message": "Account not exists!"
        }, 400
        if args["username"]:
            if account.username != args["username"]:
                user: Account = Account.query.filter_by(username=args["username"]).first()
                if user:
                    return {
                    "statusCode": 400,
                    "message": "Account existed!"
                }, 400
            account.username = args["username"]
        if args["password"]:
            password = bcrypt.hashpw(str.encode(args["password"], encoding='UTF-8'), bcrypt.gensalt())
            account.password = password=password.decode('UTF-8')
        if args["is_active"]:
            account.is_active = args["is_active"]
        
        db.session.commit()
        return {
            "statusCode": 200,
            "message": "Update account success!"
        }, 200


class MeResource(Resource):
    # APi get current account
    @token_required
    def get(self, current_user, *args, **kwargs):
        return {
            "statusCode": 200,
            "message": "Get all users",
            "results": {
                "id": current_user.id,
                "username": current_user.username,
                "is_admin": current_user.is_admin,
                "is_active": current_user.is_active,
                "created_at": current_user.created_at.strftime("%Y-%m-%d")
            }
        }, 200