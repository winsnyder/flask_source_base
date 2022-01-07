from app import db
from app.jwt import token_required
from model.topic import Topic
from flask_restful import Resource, reqparse, fields

parser = reqparse.RequestParser()
parser.add_argument("summary", type=str)
parser.add_argument("content", type=str)

def topicReponse(item):
    return {
        "id": item.id,
        "summary": item.summary,
        "content": item.content,
        "created_at": item.created_at.strftime("%Y-%m-%d")
    }


class TopicListResource(Resource):

    def get(self, *args, **kwargs):
        topics = Topic.query.all()
        data_response = [topicReponse(item) for item in topics]
        return {
            "statusCode": 200,
            "message": "Get all topic",
            "results": data_response
        }, 200

class TopicResource(Resource):

    def get(self, *args, **kwargs):
        topic = Topic.query.filter_by(id=kwargs["topic_id"]).first()
        if not topic:
            return {
            "statusCode": 400,
            "message": "Topic not exists!"
        }, 400
        return {
            "statusCode": 200,
            "message": "Get detail topic success",
            "results": topicReponse(topic)
        }

    @token_required
    def post(self, current_user, *args, **kwargs):
        args = parser.parse_args()
        topic = Topic(
            summary=args["summary"],
            content=args["content"]
        )
        db.session.add(topic)
        db.session.commit()
        return {
            "statusCode": 201,
            "message": "Get detail topic success",
            "results": topicReponse(topic)
        }, 201

    @token_required
    def put(self, current_user, *args, **kwargs):
        args = parser.parse_args()
        topic = Topic.query.filter_by(id=kwargs["topic_id"]).first()
        if not topic:
            return {
            "statusCode": 400,
            "message": "Topic not exists!"
        }, 400
        if args["summary"]:
            topic.summary = args["summary"]
        if args["content"]:
            topic.content = args["content"]
        db.session.commit()
        return {
            "statusCode": 200,
            "message": "Update topic success!"
        }, 200

    @token_required
    def delete(self, current_user, *args, **kwargs):
        topic = Topic.query.filter_by(id=kwargs["topic_id"]).first()
        if not topic:
            return {
            "statusCode": 400,
            "message": "Topic not exists!"
        }, 400
        db.session.delete(topic)
        db.session.commit()
        return {
            "statusCode": 204,
            "message": "Delete topic success!"
        }, 200
