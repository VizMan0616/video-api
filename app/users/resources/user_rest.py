from flask_restful import Resource, reqparse, marshal_with
from ...schemas import UserSchema
from ...models import User, Channel
from ... import db
from datetime import datetime
from ...common.constants import SUCCESS_DICT
from ...common.status_handlers import Success


class UserREST(Resource):
    def get(self):
        return UserSchema(many=True).dump(User.query.all())

    @marshal_with(SUCCESS_DICT)
    def post(self):
        args = self.create_args()

        user = User(username=args['username'],
                    name=args['firstName'],
                    last_name=args['lastName'],
                    birth_date=datetime.strptime(
                        args['birthDate'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                    sex_id=args['sexId'],
                    email=args['email'],
                    password=args['password'])
        db.session.add(user)
        db.session.commit()

        channel = Channel(channel_name=user.username,
                          owner_id=user.id, creation_date=datetime.utcnow())

        db.session.add(channel)
        db.session.commit()

        return Success(data=user.username, message="User added successfully", status_code=201, from_request="POST"), 201

    def create_args(self):
        post_args = reqparse.RequestParser()
        post_args.add_argument(
            "username", help="The USERNAME is required", required=True)
        post_args.add_argument(
            "firstName", help="The FIRST NAME is required", required=True)
        post_args.add_argument(
            "lastName", help="The LAST NAME is required", required=True)
        post_args.add_argument(
            "birthDate", help="The BIRTH DATE is required", required=True)
        post_args.add_argument(
            "sexId", help="The SEX ID is required", required=True)
        post_args.add_argument(
            "email", help="The EMAIL is required", required=True)
        post_args.add_argument(
            "password", help="The PASSWORD is required", required=True)

        return post_args.parse_args()
