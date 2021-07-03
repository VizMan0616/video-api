from flask_restful import Resource, reqparse, marshal_with, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...models import Video
from ... import db
from ...common.constants import SUCCESS_DICT
from ...common.status_handlers import Success


class ReproductionREST(Resource):
    @marshal_with(SUCCESS_DICT)
    @jwt_required()
    def put(self, video_id):
        video = Video.get_video_id(video_id)

        if not video:
            abort(404, message="The video reproduction, does not exit")

        video.details.reproduced()
        db.session.add(video.details)
        db.session.commit()

        return Success(data=video.video_title, message="Video reproduced sucessfully", status_code=200, from_request="PUT")
