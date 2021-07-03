from flask_restful import Resource
from ...schemas import UserSchema
from ...models import User


class UsersREST(Resource):
    def get(self):
        return UserSchema(many=True).dump(User.get_users())

