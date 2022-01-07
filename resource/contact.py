from app import db
from app.jwt import token_required
from model.contact import Contact
from flask_restful import Resource, reqparse

from model.post import Post

parser = reqparse.RequestParser()
parser.add_argument("content", type=str)
parser.add_argument("email", type=str)
parser.add_argument("phone", type=str)
parser.add_argument("fullname", type=str)
parser.add_argument("post_id", type=str)

def contactReponse(item):
    return {
        "id": item.id,
        "fullname": item.fullname,
        "content": item.content,
        "phone": item.phone,
        "email": item.email,
        "created_at": item.created_at.strftime("%Y-%m-%d")
    }


class ContactListResource(Resource):

    def get(self, *args, **kwargs):
        contacts = Contact.query.order_by(Contact.id.desc())
        data_response = [contactReponse(item) for item in contacts]
        return {
            "statusCode": 200,
            "message": "Get all contact",
            "results": data_response
        }, 200

class ContactResource(Resource):

    def get(self, *args, **kwargs):
        contact = Contact.query.filter_by(id=kwargs["contact_id"]).first()
        if not contact:
            return {
            "statusCode": 400,
            "message": "Contact not exists!"
        }, 400
        return {
            "statusCode": 200,
            "message": "Get detail comment success",
            "results": contactReponse(contact)
        }

    def post(self, *args, **kwargs):
        args = parser.parse_args()

        contact = Contact(
            fullname=args["fullname"],
            email=args["email"],
            phone=args["phone"],
            content=args["content"]
        )
        db.session.add(contact)
        db.session.commit()
        return {
            "statusCode": 201,
            "message": "create contact success",
            "results": contactReponse(contact)
        }, 201


    @token_required
    def delete(self, current_user, *args, **kwargs):
        contact = Contact.query.filter_by(id=kwargs["contact_id"]).first()
        if not contact:
            return {
            "statusCode": 400,
            "message": "Contact not exists!"
        }, 400
        
        db.session.delete(contact)
        db.session.commit()
        return {
            "statusCode": 204,
            "message": "Delete contact success!"
        }, 200
