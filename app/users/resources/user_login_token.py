from flask import jsonify
from flask_restful import Resource, reqparse, abort, marshal_with
from flask_jwt_extended import create_access_token, set_access_cookies
from ...models import User
from ... import jwt
from ...common.status_handlers import Token
from ...common.constants import ACCESS_TOKEN_DICT


class LoginToken(Resource):
    @marshal_with(ACCESS_TOKEN_DICT)
    def post(self):
        args = self.create_args()

        user = User.get_user_email(args['email'])
        if not user and not user.verify_password(args['password']):
            abort(401, message='Wrong USERNAME or PASSWORD')

        access_token = create_access_token(identity=user)
        return Token(status_code=201, token=access_token)

    def create_args(self):
        post_args = reqparse.RequestParser()
        post_args.add_argument(
            "email", help="The EMAIL is required", required=True)
        post_args.add_argument(
            "password", help="The PASSWORD is required", required=True)

        return post_args.parse_args()
