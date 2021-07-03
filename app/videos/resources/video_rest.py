from flask_restful import Resource, reqparse, marshal_with, abort
from flask_jwt_extended import jwt_required, current_user
from werkzeug.datastructures import FileStorage
from datetime import datetime as dt
from ...models import Video, Details
from ...schemas import VideoSchema
from ... import db
from ...common.constants import SUCCESS_DICT
from ...common.status_handlers import Success
from ...common.utils import save_video


class VideoREST(Resource):
    @jwt_required()
    def get(self):
        return VideoSchema(many=True).dump(current_user.user_channel.videos)
        #get_args = reqparse.RequestParser()
        # get_args.add_argument(
        #    "videoQuery", type=str, help="The QUERY is required", required=True)
        #args = get_args.parse_args()

        # return Video.get_matched_videos(args['videoQuery'])

    @marshal_with(SUCCESS_DICT)
    @jwt_required()
    def post(self):
        args = self.create_args()

        video = Video(
            args['videoTitle'], current_user.user_channel.id, args['description'] or '')
        save_video(current_user.user_channel.channel_name,
                   args['videoTitle'], args['videoFile'])
        db.session.add(video)
        db.session.commit()

        video_details = Details(video.id)
        db.session.add(video_details)
        db.session.commit()

        return Success(data=args['videoTitle'], message="Video created successfully", status_code=201, from_request="POST"), 201

    def create_args(self):
        post_args = reqparse.RequestParser()
        post_args.add_argument(
            "videoTitle", help="The USERNAME is required", type=str, required=True)
        post_args.add_argument("description", type=str)
        post_args.add_argument(
            'videoFile', type=FileStorage, location='files', required=True)

        return post_args.parse_args()


