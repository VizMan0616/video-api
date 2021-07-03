from flask_restful import Resource, reqparse, marshal_with, abort
from flask_jwt_extended import jwt_required, current_user
from ...schemas import UserSchema
from ...models import User, Channel
from ... import db
from datetime import datetime
from ...common.constants import SUCCESS_DICT
from ...common.status_handlers import Success


class SubscribeREST(Resource):
    @marshal_with(SUCCESS_DICT)
    @jwt_required()
    def post(self):
        args = self.create_args()

        if args['channelName']:
            channel = Channel.get_channel_name(args['channelName'])
        if args['channelId']:
            channel = Channel.get_channel_id(args['channelId'])

        if not channel:
            abort(404, message="Channel or User does not exist...")
        if channel in current_user.subcribed_to:
            abort(
                409, message=f'{current_user.username} is already subscribed to {channel.channel_name}')

        current_user.subcribed_to.append(channel)
        db.session.add(current_user)
        db.session.commit()

        return Success(data=f'{current_user} > {channel.channel_name}', message="User successfully subscribedl", from_request='POST', status_code=201), 201

    @marshal_with(SUCCESS_DICT)
    @jwt_required()
    def delete(self):
        args = self.create_args()

        if args['channelName']:
            channel = Channel.get_channel_name(args['channelName'])
        if args['channelId']:
            channel = Channel.get_channel_id(args['channelId'])

        if not channel:
            abort(404, message="Channel or User does not exist...")
        if not channel in current_user.subcribed_to:
            abort(
                409, message=f"{current_user.username} is already desubscribed to {channel.channel_name}")

        current_user.subcribed_to.remove(channel)
        db.session.add(current_user)
        db.session.commit()

        return Success(data=f'{current_user} not {channel.channel_name}', message="User successfully desubscribedl", from_request='DELETE', status_code=200)

    def create_args(self):
        post_args = reqparse.RequestParser()
        post_args.add_argument("channelName", type=str)
        post_args.add_argument("channelId", type=int)

        return post_args.parse_args()
