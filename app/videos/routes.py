from flask import Blueprint, send_file, safe_join, current_app
from flask_restful import Api
from flask_jwt_extended import jwt_required, current_user

from .resources.video_rest import VideoREST
from .resources.video_param_rest import VideoParamREST
from .resources.videos_rest import VideosREST
from .resources.like_video_rest import LikeVideoREST
from .resources.reproduction_rest import ReproductionREST
from .resources.send_video_rest import SendVideo


videos_bp = Blueprint('videos', __name__)
videos_api = Api(videos_bp)


# @videos_api.representation('application/octet-stream')
# def send_file(data, code, headers):
#    filepath = safe_join(data["directory"], data["filename"])
#
#   response = send_file(
#        filename_or_fp=filepath,
#        mimetype="application/octet-stream",
#        as_attachment=True,
#        attachment_filename=data["filename"]
#    )
#    return response


videos_api.add_resource(VideoREST, '/video')
videos_api.add_resource(VideoParamREST, '/video/<int:video_id>')
videos_api.add_resource(VideosREST, '/videos')
videos_api.add_resource(LikeVideoREST, '/video/<int:video_id>/like')
videos_api.add_resource(
    ReproductionREST, '/video/<int:video_id>/reproduction')
videos_api.add_resource(SendVideo, '/video/download/<filename>')



