from itsdangerous import json
from app import db
from app.jwt import token_required
from models.task import Task
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument("project_id", type=str)
parser.add_argument("data", type=str)


def taskReponse(item):
    return {
        "id": item.id,
        "project_id": item.project_id,
        "data": item.data,
        "created_at": item.created_at.strftime("%Y-%m-%d")
    }


class TaskListResource(Resource):

    def get(self, *args, **kwargs):
        tasks = Task.query.all()
        data_response = [taskReponse(item) for item in tasks]
        return {
            "statusCode": 200,
            "message": "Get all task",
            "results": data_response
        }, 200


class TaskResource(Resource):

    def get(self, *args, **kwargs):
        task = Task.query.filter_by(id=kwargs["task_id"]).first()
        if not task:
            return {
                "statusCode": 400,
                "message": "Post not exists!"
            }, 400
        return {
            "statusCode": 200,
            "message": "Get detail post success",
            "results": taskReponse(task)
        }

    @token_required
    def post(self, current_user, *args, **kwargs):
        args = parser.parse_args()
        task = Task(
            project_id=args["project_id"],
            data=args["data"],
        )
        db.session.add(task)
        db.session.commit()
        return {
            "statusCode": 201,
            "message": "Add project done",
            "results": taskReponse(task)
        }, 201

    @token_required
    def put(self, current_user, *args, **kwargs):
        args = parser.parse_args()
        task = Task.query.filter_by(id=kwargs["task_id"]).first()
        if not task:
            return {
                "statusCode": 400,
                "message": "Task not exists!"
            }, 400
        if args["data"]:
            task.data = args["data"]
        db.session.commit()
        return {
            "statusCode": 200,
            "message": "Update task success!"
        }, 200

    @token_required
    def delete(self, current_user, *args, **kwargs):
        task = Task.query.filter_by(id=kwargs["task_id"]).first()
        if not task:
            return {
                "statusCode": 400,
                "message": "Project not exists!"
            }, 400
        db.session.delete(task)
        db.session.commit()
        return {
            "statusCode": 204,
            "message": "Delete task success!"
        }, 204
