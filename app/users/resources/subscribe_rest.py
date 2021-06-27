from flask_restful import Resource, reqparse, marshal_with, abort
from ...schemas import UserSchema
from ...models import User, Channel
from ... import db
from datetime import datetime
from ...common.constants import SUCCESS_DICT
from ...common.status_handlers import Success


class SubscribeREST(Resource):
    @marshal_with(SUCCESS_DICT)
    def put(self, channel_id):
        args = self.create_args()

        user = User.query.filter_by(username=args['username']).first()
        channel = Channel.query.filter_by(id=channel_id).first()

        if not user or not channel:
            abort(404, message="Channel or User does not exist...")
        if channel in user.subcribed_to:
            abort(
                409, message=f'{user.username} is already subscribed to {channel.channel_name}')

        user.subcribed_to.append(channel)
        db.session.add(user)
        db.session.commit()

        return Success(data=f'{args["username"]} > {channel.channel_name}', message="User successfully subscribedl", from_request='PUT', status_code=200)

    @marshal_with(SUCCESS_DICT)
    def delete(self, channel_id):
        args = self.create_args()

        user = User.query.filter_by(username=args['username']).first()
        channel = Channel.query.filter_by(id=channel_id).first()

        if not user or not channel:
            abort(404, message="Channel or User does not exist...")
        if not channel in user.subcribed_to:
            abort(
                409, message=f"{user.username} is already desubscribed to {channel.channel_name}")

        user.subcribed_to.remove(channel)
        db.session.add(user)
        db.session.commit()

        return Success(data=f'{args["username"]} x {channel.channel_name}', message="User successfully desubscribedl", from_request='PUT', status_code=200)

    def create_args(self):
        post_args = reqparse.RequestParser()
        post_args.add_argument(
            "username", help="The USERNAME is required", required=True)

        return post_args.parse_args()
