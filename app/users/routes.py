from flask import Blueprint
from flask_restful import Api

from .resources.user_rest import UserREST
from .resources.subscribe_rest import SubscribeREST
from .resources.user_login_token import LoginToken
#from .resources.user_logout_token import LogoutToken

users_bp = Blueprint('users', __name__)
users_api = Api(users_bp)

users_api.add_resource(UserREST, '/user')
users_api.add_resource(SubscribeREST, '/user/subscription')
users_api.add_resource(LoginToken, '/user/login')
#users_api.add_resource(LogoutToken, '/user/logout')
