from flask import Blueprint
from flask_restful import Api

from .resources.videos_rest import VideosREST

videos_bp = Blueprint('videos', __name__)
videos_api = Api(videos_bp)

videos_api.add_resource(VideosREST, '/videos')
