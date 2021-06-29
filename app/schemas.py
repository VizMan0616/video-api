from .models import *
from . import ma


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    first_name = ma.auto_field(data_key='firstName')
    last_name = ma.auto_field(data_key='lastName')
    birth_date = ma.auto_field(data_key='birthDate')
    sex = ma.Nested('SexSchema', only=["sex_name"])

    email = ma.auto_field()
    password = ma.auto_field()
    user_channel = ma.Nested(
        'ChannelSchema', data_key='userChannel', exclude=['owner'])
    subcribed_to = ma.Nested(
        'ChannelSchema', daya_key='subcribedTo', many=True, only=['id', 'channel_name'])
    playlists = ma.Nested('PlaylistSchema', many=True,
                          exclude=['playlist_of'])


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
    videos = ma.Nested('VideoSchema', many=True, exclude=['video_of'])


class PlaylistSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Playlist

    id = ma.auto_field()
    playlist_name = ma.auto_field(data_key='playlistName')
    playlist_of = ma.Nested(
        UserSchema, data_key='playlistOf', only=['id', 'username'])


class VideoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Video

    id = ma.auto_field()
    video_title = ma.auto_field(data_key='videoTitle')
    release_date = ma.auto_field(data_key='releaseDate')
    description = ma.auto_field()
    details = ma.Nested('DetailsSchema', exclude=['video'])
    video_of = ma.Nested(
        ChannelSchema, data_key='videoOf', only=['id', 'channel_name'])


class DetailsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Details

    id = ma.auto_field()
    likes = ma.auto_field()
    dislikes = ma.auto_field()
    reproductions = ma.auto_field()

    video = ma.Nested(VideoSchema, exclude=['details'])







