from .models import *
from . import ma
from marshmallow import fields


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    name = ma.auto_field(data_key='firstName')
    last_name = ma.auto_field(data_key='lastName')
    birth_date = ma.auto_field(data_key='birthDate')
    sex = ma.Nested('SexSchema', only=["sex_name"])

    email = ma.auto_field()
    password = ma.auto_field()
    user_channel = ma.Nested(
        'ChannelSchema', data_key='userChannel', exclude=['owner'])
    subcribed_to = ma.Nested(
        'ChannelSchema', daya_key='subcribedTo', many=True, only=['id', 'channel_name'])


class SexSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Sex

    id = ma.auto_field()
    sex_name = ma.auto_field(data_key='sexName')
    users = ma.Nested(UserSchema, many=True, exclude=['sex'])


class ChannelSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Channel

    id = ma.auto_field()
    channel_name = ma.auto_field(data_key='chanelName')
    owner = ma.Nested(UserSchema, exclude=['user_channel'])
    creation_date = ma.auto_field(data_key='creationDate')
    subscriptions = ma.Nested(
        UserSchema, many=True, only=['id', 'username'])







