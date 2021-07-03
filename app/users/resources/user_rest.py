from flask_restful import Resource, reqparse, marshal_with
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime as dt
from ...schemas import UserSchema
from ...models import User, Channel
from ... import db
from ...common.constants import SUCCESS_DICT
from ...common.status_handlers import Success
from ...common.utils import create_user_folder


class UserREST(Resource):
    @jwt_required()
    def get(self):
        return UserSchema().dump(current_user)

    @marshal_with(SUCCESS_DICT)
    def post(self):
        args = self.create_args()

        user = User(args['username'], args['firstName'], args['lastName'], dt.strptime(
            args['birthDate'], '%Y-%m-%dT%H:%M:%S.%fZ'), args['sexId'], args['email'], args['password'])
        create_user_folder(user.username)
        db.session.add(user)
        db.session.commit()

        channel = Channel(user.username, user.id)
        db.session.add(channel)
        db.session.commit()
        return Success(data=user.username, message="User added successfully", status_code=201, from_request="POST"), 201

    @marshal_with(SUCCESS_DICT)
    @jwt_required()
    def put(self):
        args = self.create_optional_args()

        current_user.username = args['username'] or current_user.username
        current_user.first_name = args['firstName'] or current_user.first_name
        current_user.last_name = args['lastName'] or current_user.last_name

        current_user.user_channel.channel_name = args['username'] or current_user.username

        db.session.add(current_user)
        db.session.commit()

        return Success(data=current_user.username, message="User updated successfully", status_code=200, from_request="PUT")

    def create_args(self):
        post_args = reqparse.RequestParser()
        post_args.add_argument(
            "username", help="The USERNAME is required", type=str, required=True)
        post_args.add_argument(
            "firstName", help="The FIRST NAME is required", type=str, required=True)
        post_args.add_argument(
            "lastName", help="The LAST NAME is required", type=str, required=True)
        post_args.add_argument(
            "birthDate", help="The BIRTH DATE is required", type=str, required=True)
        post_args.add_argument(
            "sexId", help="The SEX ID is required", type=int, required=True)
        post_args.add_argument(
            "email", help="The EMAIL is required", type=str, required=True)
        post_args.add_argument(
            "password", help="The PASSWORD is required", type=str, required=True)

        return post_args.parse_args()

    def create_optional_args(self):
        put_args = reqparse.RequestParser()
        put_args.add_argument("username", type=str)
        put_args.add_argument("firstName", type=str)
        put_args.add_argument("lastName", type=str)

        return put_args.parse_args()
