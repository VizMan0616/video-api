from flask_restful import Resource, reqparse, abort, marshal_with
from ... import db
from ...models import Video, Details
from ...schemas import VideoSchema
from ...common.constants import SUCCESS_DICT
from ...common.status_handlers import Success


class VideosREST(Resource):
    def get(self):
        return VideoSchema(many=True).dump(Video.get_videos())

    @marshal_with(SUCCESS_DICT)
    def post(self):
        args = self.create_args()

        video = Video(args['videoTitle'], args['channelId'],
                      args['description'] or '')
        db.session.add(video)
        db.session.commit()

        details = Details(video.id)
        db.session.add(details)
        db.session.commit()

        return Success(data=video.video_title, message="Video successfully uploaded", status_code=201)

    def create_args(self):
        post_parse = reqparse.RequestParser()

        post_parse.add_argument(
            'videoTitle', help='The TITLE is required', required=True)
        post_parse.add_argument('description')
        post_parse.add_argument(
            'channelId', help='The CHANNEL ID is required', required=True)

        return post_parse.parse_args()


