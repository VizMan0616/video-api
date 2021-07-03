from flask import current_app, send_from_directory
from flask_restful import Resource, reqparse, marshal_with, abort

from ...models import Video, Details
from ...schemas import VideoSchema
from ... import db


class SendVideo(Resource):
    def get(self, filename):
        get_args = reqparse.RequestParser()
        get_args.add_argument('channelName', help='jeje', required=True)
        args = get_args.parse_args()
        return send_from_directory(f'{current_app.root_path}\\static\\videos\\{args["channelName"]}', filename)
