from flask import jsonify
from flask_restful import Resource, reqparse, abort, marshal_with
from flask_jwt_extended import create_access_token
from ...models import User
from ... import jwt
from ...common.status_handlers import Token
from ...common.constants import ACCESS_TOKEN_DICT


class LoginToken(Resource):
    @marshal_with(ACCESS_TOKEN_DICT)
    def post(self):
        args = self.create_args()

        user = User.get_user_email(args['email'])
        if not user:
            abort(404, message='User does not exist')

            if not user.verify_password(args['password']):
                abort(401, message='Password does not match')

        access_token = create_access_token(identity=user)
        return Token(status_code=201, token=access_token), 201

    def create_args(self):
        post_args = reqparse.RequestParser()
        post_args.add_argument(
            "email", help="The EMAIL is required", type=str, required=True)
        post_args.add_argument(
            "password", help="The PASSWORD is required", type=str, required=True)

        return post_args.parse_args()
