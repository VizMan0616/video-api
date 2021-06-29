from flask_restful import Resource, reqparse, marshal_with
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime as dt
from ...schemas import UserSchema
from ...models import User, Channel
from ... import db
from ...common.constants import SUCCESS_DICT
from ...common.status_handlers import Success


class UserREST(Resource):
    @jwt_required()
    def get(self):
        return UserSchema().dump(current_user)

    @marshal_with(SUCCESS_DICT)
    def post(self):
        args = self.create_args()

        user = User(args['username'], args['firstName'], args['lastName'], dt.strptime(
            args['birthDate'], '%Y-%m-%dT%H:%M:%S.%fZ'), args['sexId'], args['email'], args['password'])
        db.session.add(user)
        db.session.commit()

        channel = Channel(user.username, user.id)
        db.session.add(channel)
        db.session.commit()

        return Success(data=user.username, message="User added successfully", status_code=201, from_request="POST"), 201

    @marshal_with(SUCCESS_DICT)
    @jwt_required()
    def put(self, user_id):
        args = self.create_optional_args()

        current_user.username = args['username'] or current_user.username
        current_user.name = args['firstName'] or current_user.name
        current_user.last_name = args['lastName'] or current_user.last_name

        if args['birthDate']:
            current_user.birth_date = datetime.strptime(
                args['birthDate'], '%Y-%m-%dT%H:%M:%S.%fZ')

        user.sex_id = args['sexId'] or current_user.sex_id

        user.user_channel.channel_name = args['username'] or user.username

        db.session.add(user)
        db.session.commit()

        return Success(data=user.username, message="User updated successfully", status_code=200, from_request="PUT"), 200

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

    def create_optional_args(self):
        put_args = reqparse.RequestParser()
        put_args.add_argument("username")
        put_args.add_argument("firstName")
        put_args.add_argument("lastName")
        put_args.add_argument("birthDate")
        put_args.add_argument("sexId")

        return put_args.parse_args()
