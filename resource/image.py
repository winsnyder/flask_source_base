from app import db
from app.jwt import token_required
from models.image import Image
from flask_restful import Resource, reqparse, fields

parser = reqparse.RequestParser()
parser.add_argument("title", type=str)
parser.add_argument("url", type=str)
parser.add_argument("keyword", type=str)


def imageReponse(item):
    return {
        "id": item.id,
        "title": item.title,
        "url": item.url,
        "created_at": item.created_at.strftime("%Y-%m-%d")
    }


class ImageListResource(Resource):

    def get(self, *args, **kwargs):
        args = parser.parse_args()
        if args['keyword']:
            images = Image.query.filter(
                (Image.title.ilike(f'%{args["keyword"]}%'))
            ).order_by(Image.id.desc())
        if not args["keyword"]:
            images = Image.query.order_by(Image.id.desc())
        data_response = [imageReponse(item) for item in images]
        return {
            "statusCode": 200,
            "message": "Get all post",
            "results": data_response
        }, 200


class ImageResource(Resource):

    def get(self, *args, **kwargs):
        image = Image.query.filter_by(id=kwargs["image_id"]).first()
        if not image:
            return {
                "statusCode": 400,
                "message": "Image not exists!"
            }, 400
        return {
            "statusCode": 200,
            "message": "Get detail image success",
            "results": imageReponse(image)
        }

    @token_required
    def post(self, current_user, *args, **kwargs):
        args = parser.parse_args()
        image = Image(
            title=args["title"],
            url=args["url"]
        )
        db.session.add(image)
        db.session.commit()
        return {
            "statusCode": 201,
            "message": "Get detail image success",
            "results": imageReponse(image)
        }, 201

    @token_required
    def put(self, current_user, *args, **kwargs):
        args = parser.parse_args()
        image = Image.query.filter_by(id=kwargs["image_id"]).first()
        if not image:
            return {
                "statusCode": 400,
                "message": "Image not exists!"
            }, 400
        if args["title"]:
            image.title = args["title"]
        if args["url"]:
            image.url = args["url"]
        db.session.commit()
        return {
            "statusCode": 200,
            "message": "Update image success!"
        }, 200

    @token_required
    def delete(self, current_user, *args, **kwargs):
        image = Image.query.filter_by(id=kwargs["image_id"]).first()
        if not image:
            return {
                "statusCode": 400,
                "message": "Image not exists!"
            }, 400
        db.session.delete(image)
        db.session.commit()
        return {
            "statusCode": 204,
            "message": "Delete image success!"
        }, 200
