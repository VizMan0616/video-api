from flask import Blueprint
from flask_restful import Api

from .resources.user_rest import UserREST
from .resources.user_param_rest import UserParamREST
from .resources.subscribe_rest import SubscribeREST

users_bp = Blueprint('users', __name__)
users_api = Api(users_bp)

users_api.add_resource(UserREST, '/user')
users_api.add_resource(UserParamREST, '/user/<int:user_id>')
users_api.add_resource(SubscribeREST, '/user/subscription/<int:channel_id>')
