from app import db
from app.jwt import token_required
from models.project import Project
from models.task import Task
from flask_restful import Resource, reqparse, fields
import json

parser = reqparse.RequestParser()
parser.add_argument("project_name", type=str)
parser.add_argument("tag", type=str)
parser.add_argument("deadline", type=str)
parser.add_argument("keyword", type=str)


def projectReponse(item):
    return {
        "id": item.id,
        "project_name": item.project_name,
        "tag": item.tag,
        "deadline": item.deadline,
        "created_at": item.created_at.strftime("%Y-%m-%d")
    }


class ProjectListResource(Resource):

    def get(self, *args, **kwargs):
        args = parser.parse_args()
        if args['keyword']:
            projects = Project.query.filter(
                (Project.project_name.ilike(f'%{args["keyword"]}%')) |
                (Project.tag.ilike(f'%{args["keyword"]}%'))
            ).order_by(Project.id.desc())
        if not args["keyword"]:
            projects = Project.query.order_by(Project.id.desc())
        data_response = [projectReponse(item) for item in projects]
        return {
            "statusCode": 200,
            "message": "Get all post",
            "results": data_response
        }, 200


class ProjectResource(Resource):

    def get(self, *args, **kwargs):
        project = Project.query.filter_by(id=kwargs["project_id"]).first()
        if not project:
            return {
                "statusCode": 400,
                "message": "Post not exists!"
            }, 400
        return {
            "statusCode": 200,
            "message": "Get detail post success",
            "results": projectReponse(project)
        }

    @token_required
    def post(self, current_user, *args, **kwargs):
        args = parser.parse_args()
        project = Project(
            project_name=args["project_name"],
            tag=args["tag"],
            deadline=args["deadline"],
        )
        db.session.add(project)
        db.session.commit()

        # Create task follow
        task = Task(
            project_id=project.id,
            data=json.dumps({
                "lanes": []
            }),
        )
        db.session.add(task)
        db.session.commit()
        return {
            "statusCode": 201,
            "message": "Add project done",
            "results": projectReponse(project)
        }, 201

    @token_required
    def put(self, current_user, *args, **kwargs):
        args = parser.parse_args()
        project = Project.query.filter_by(id=kwargs["project_id"]).first()
        if not project:
            return {
                "statusCode": 400,
                "message": "Topic not exists!"
            }, 400
        if args["project_name"]:
            project.project_name = args["project_name"]
        if args["tag"]:
            project.tag = args["tag"]
        if args["deadline"]:
            project.deadline = args["deadline"]
        db.session.commit()
        return {
            "statusCode": 200,
            "message": "Update topic success!"
        }, 200

    @token_required
    def delete(self, current_user, *args, **kwargs):
        project = Project.query.filter_by(id=kwargs["project_id"]).first()
        if not project:
            return {
                "statusCode": 400,
                "message": "Project not exists!"
            }, 400
        db.session.delete(project)
        db.session.commit()
        return {
            "statusCode": 204,
            "message": "Delete project success!"
        }, 204
