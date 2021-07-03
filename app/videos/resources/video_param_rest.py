from flask_restful import Resource, reqparse, marshal_with, abort
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime as dt
from ...models import Video, Details
from ...schemas import VideoSchema
from ... import db
from ...common.constants import SUCCESS_DICT
from ...common.status_handlers import Success
from ...common.utils import delete_video, rename_video


class VideoParamREST(Resource):
    @marshal_with(SUCCESS_DICT)
    @jwt_required()
    def put(self, video_id):
        args = self.create_args()

        video = Video.get_video_id(video_id)

        if not video:
            abort(
                404, message="The video you are trying to modify, does not exit, yet...")

        rename_video(current_user.username,
                     video.video_title, args['videoTitle'])
        video.video_title = args['videoTitle'] or video.video_title
        video.description = args['description'] or video.description
        db.session.add(video)
        db.session.commit()

        return Success(data=args['videoTitle'], message="Video updated successfully", status_code=200, from_request="PUT")

    @marshal_with(SUCCESS_DICT)
    @jwt_required()
    def delete(self, video_id):
        video = Video.get_video_id(video_id)

        if not video:
            abort(404, message="The video you are trying to delete, does not exit")

        db.session.delete(video)
        delete_video(current_user.username, video.video_title)
        db.session.commit()
        return Success(data='', message="Video deleted successfully", status_code=200, from_request="DELETE")

    def create_args(self):
        put_args = reqparse.RequestParser()
        put_args.add_argument(
            "videoTitle", type=str)
        put_args.add_argument("description", type=str)

        return put_args.parse_args()


