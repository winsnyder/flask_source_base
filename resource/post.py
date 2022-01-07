import werkzeug
import base64
from app import db
from app.jwt import token_required
from model.post import Post
from flask_restful import Resource, reqparse

from model.topic import Topic

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

parser = reqparse.RequestParser()
parser.add_argument("title", type=str)
parser.add_argument("summary", type=str)
parser.add_argument("content", type=str)
parser.add_argument("topic_id", type=str)
parser.add_argument("keyword", type=str)
parser.add_argument('file',
                    type=werkzeug.datastructures.FileStorage,
                    location='files',
                    help='provide a file')

def postReponse(item):
    return {
        "id": item.id,
        "title": item.title,
        "image": item.image,
        "is_publish": item.is_publish,
        "author": item.account.username,
        "topic_id": item.topic.id,
        "topic_name": item.topic.content,
        "summary": item.summary,
        "content": item.content,
        "created_at": item.created_at.strftime("%Y-%m-%d")
    }


class PostListResource(Resource):

    def get(self, *args, **kwargs):
        args = parser.parse_args()
        if args["topic_id"]:
            posts = Post.query.filter_by(
                topic_id=int(args["topic_id"])
            ).order_by(Post.id.desc())
        if args['keyword']:
            posts = Post.query.filter(
                (Post.title.ilike(f'%{args["keyword"]}%')) |
                (Post.summary.ilike(f'%{args["keyword"]}%')) |
                (Post.content.ilike(f'%{args["keyword"]}%'))
            ).order_by(Post.id.desc())
        if not args["topic_id"] and not args["keyword"]:
            posts = Post.query.order_by(Post.id.desc())
        data_response = [postReponse(item) for item in posts]
        return {
            "statusCode": 200,
            "message": "Get all post",
            "results": data_response
        }, 200

class PostResource(Resource):

    def get(self, *args, **kwargs):
        post = Post.query.filter_by(id=kwargs["post_id"]).first()
        if not post:
            return {
            "statusCode": 400,
            "message": "Post not exists!"
        }, 400
        return {
            "statusCode": 200,
            "message": "Get detail post success",
            "results": postReponse(post)
        }

    @token_required
    def post(self, current_user, *args, **kwargs):
        args = parser.parse_args()
        file = args["file"]
        if file and allowed_file(file.filename):
            image_string = base64.b64encode(file.read())
        else:
            return {
                "statusCode": 400,
                "message": "File is wrong format!"
            }, 400
        topic = Topic.query.filter_by(id=int(args["topic_id"])).first()
        post = Post(
            title=args["title"],
            image=image_string.decode('utf-8'),
            summary=args["summary"],
            content=args["content"],
            account=current_user,
            topic=topic
        )
        db.session.add(post)
        db.session.commit()
        return {
            "statusCode": 201,
            "message": "Get detail topic success",
            "results": postReponse(post)
        }, 201

    @token_required
    def put(self, current_user, *args, **kwargs):
        args = parser.parse_args()
        post = Post.query.filter_by(id=kwargs["post_id"]).first()
        if not current_user.is_admin:
            if current_user.id != post.account_id:
                return {
                "statusCode": 400,
                "message": "Don't have permission!"
            }, 400
        if not post:
            return {
            "statusCode": 400,
            "message": "Post not exists!"
        }, 400
        if args["topic_id"]:
            topic = Topic.query.filter_by(id=int(args["topic_id"])).first()
            post.topic = topic
        if args["title"]:
            post.title = args["title"]
        if args["file"]:
            file = args["file"]
            if file and allowed_file(file.filename):
                image_string = base64.b64encode(file.read())
            else:
                return {
                    "statusCode": 400,
                    "message": "File is wrong format!"
                }, 400
            image=image_string.decode('utf-8'),
        if args["summary"]:
            post.summary = args["summary"]
        if args["content"]:
            post.content = args["content"]
        db.session.commit()
        return {
            "statusCode": 200,
            "message": "Update post success!"
        }, 200

    @token_required
    def delete(self, current_user, *args, **kwargs):
        post = Post.query.filter_by(id=kwargs["post_id"]).first()
        if not current_user.is_admin:
            if current_user.id != post.account_id:
                return {
                "statusCode": 400,
                "message": "Don't have permission!"
            }, 400
        if not post:
            return {
            "statusCode": 400,
            "message": "Post not exists!"
        }, 400
        db.session.delete(post)
        db.session.commit()
        return {
            "statusCode": 204,
            "message": "Delete post success!"
        }, 200
