from flask_restful import Resource, reqparse, abort, marshal_with
from ...schemas import UserSchema
from ...models import User, Channel
from ... import db
from datetime import datetime
from ...common.constants import SUCCESS_DICT
from ...common.status_handlers import Success


class UserParamREST(Resource):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()

        if not user:
            abort(404, message="User does not exit on the database, yet...")

        return UserSchema().dump(user)

    @marshal_with(SUCCESS_DICT)
    def put(self, user_id):
        args = self.create_args()
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="Required user does not exist...")

        user.username = args['username'] or user.username
        user.name = args['firstName'] or user.name
        user.last_name = args['lastName'] or user.last_name

        if args['birthDate']:
            user.birth_date = datetime.strptime(
                args['birthDate'], '%Y-%m-%dT%H:%M:%S.%fZ')

        user.sex_id = args['sexId'] or user.sex_id
        user.email = args['email'] or user.email
        user.password = args['password'] or user.password

        user.user_channel.channel_name = args['username'] or user.username

        db.session.add(user)
        db.session.commit()

        return Success(data=user.username, message="User updated successfully", status_code=200, from_request="PUT"), 200

    
    def create_args(self):
        put_args = reqparse.RequestParser()
        put_args.add_argument("username")
        put_args.add_argument("firstName")
        put_args.add_argument("lastName")
        put_args.add_argument("birthDate")
        put_args.add_argument("sexId")
        put_args.add_argument("email")
        put_args.add_argument("password")

        return put_args.parse_args()

