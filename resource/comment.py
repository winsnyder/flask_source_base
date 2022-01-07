from app import db
from app.jwt import token_required
from model.comment import Comment
from flask_restful import Resource, reqparse

from model.post import Post

parser = reqparse.RequestParser()
parser.add_argument("content", type=str)
parser.add_argument("author", type=str)
parser.add_argument("post_id", type=int)

def commentReponse(item):
    return {
        "id": item.id,
        "author": item.author,
        "content": item.content,
        "created_at": item.created_at.strftime("%Y-%m-%d")
    }


class CommentListResource(Resource):

    def get(self, *args, **kwargs):
        args = parser.parse_args()
        comments = Comment.query.filter_by(post_id=int(args["post_id"])).order_by(Comment.id.desc())
        data_response = [commentReponse(item) for item in comments]
        return {
            "statusCode": 200,
            "message": "Get all comments",
            "results": data_response
        }, 200

class CommentResource(Resource):

    def get(self, *args, **kwargs):
        comment = Comment.query.filter_by(id=kwargs["comment_id"]).first()
        if not comment:
            return {
            "statusCode": 400,
            "message": "Comment not exists!"
        }, 400
        return {
            "statusCode": 200,
            "message": "Get detail comment success",
            "results": commentReponse(comment)
        }

    def post(self, *args, **kwargs):
        args = parser.parse_args()
        post = Post.query.filter_by(id=int(args["post_id"])).first()
        if not post:
            return {
            "statusCode": 400,
            "message": "Post not exists!"
        }, 400

        comment = Comment(
            author=args["author"],
            content=args["content"],
            post=post
        )
        db.session.add(comment)
        db.session.commit()
        return {
            "statusCode": 201,
            "message": "create comment success",
            "results": commentReponse(comment)
        }, 201


    @token_required
    def delete(self, current_user, *args, **kwargs):
        comment = Comment.query.filter_by(id=kwargs["comment_id"]).first()
        if not comment:
            return {
            "statusCode": 400,
            "message": "Comment not exists!"
        }, 400

        if not current_user.is_admin:
            if current_user.id != comment.post.account_id:
                return {
                "statusCode": 400,
                "message": "Don't have permission!"
            }, 400
        
        db.session.delete(comment)
        db.session.commit()
        return {
            "statusCode": 204,
            "message": "Delete comment success!"
        }, 200
