from flask_restful import Resource
from ...models import Video
from ...schemas import VideoSchema


class VideosREST(Resource):
    def get(self):
        return VideoSchema(many=True).dump(Video.get_random_videos_order())




