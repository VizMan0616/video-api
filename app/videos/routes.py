from flask import Blueprint
from flask_restful import Api

from .resources.videos_list_rest import VideosListREST

videos_bp = Blueprint('videos', __name__)
videos_api = Api(videos_bp)

videos_api.add_resource(VideosListREST, '/videos')
