from flask_restful import Resource, reqparse, marshal_with, abort
from flask_jwt_extended import jwt_required, current_user
from ...models import Video
from ... import db
from ...common.constants import SUCCESS_DICT
from ...common.status_handlers import Success


class LikeVideoREST(Resource):
    @marshal_with(SUCCESS_DICT)
    @jwt_required()
    def put(self, video_id):
        video = Video.get_video_id(video_id)

        if not video:
            abort(404, message="The video you are trying to like, does not exit")

        video.details.like()
        db.session.add(video.details)
        db.session.commit()

        return Success(data=video.video_title, message="Video liked sucessfully", status_code=200, from_request="PUT")

    @marshal_with(SUCCESS_DICT)
    @jwt_required()
    def delete(self, video_id):
        video = Video.get_video_id(video_id)

        if not video:
            abort(404, message="The video you are trying to unlike, does not exit")

        video.details.unlike()
        db.session.add(video.details)
        db.session.commit()

        return Success(data=video.video_title, message="Video is not liked anymore", status_code=200, from_request="DELETE")
