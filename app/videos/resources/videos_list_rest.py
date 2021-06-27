from flask_restful import Resource, reqparse, abort, marshal_with


class VideosListREST(Resource):
    def get(self):
        return {'yoom': 'no, yoom'}
