from flask_restful import fields

SUCCESS_DICT = {
    "fromRequest": fields.String,
    "statusCode": fields.Integer,
    "data": fields.String,
    "message": fields.String

}
