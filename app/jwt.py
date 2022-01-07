import jwt
from app import app
from flask import request
from functools import wraps
from model.account import Account

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return {
                "statusCode": 401,
                "message": "Token missing!"
            }, 401
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
            current_user = Account.query\
                .filter_by(id = data['id'])\
                .first()
        except:
            return {
                "statusCode": 401,
                "message": "Token is invalid!"
            }, 401
        instance = None
        # returns the current logged in users contex to the routes
        return f(instance, current_user, *args, **kwargs)
  
    return decorated