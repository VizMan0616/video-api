from . import db

relation_subscriber = db.Table('relationsubscriber', db.Model.metadata, db.Column(
    'user_id', db.Integer, db.ForeignKey('user.id')), db.Column('channel_id', db.Integer, db.ForeignKey('channel.id')))


# class RelationSubscriber(db.Model.metadata):
#id = db.Column(db.Integer, primary_key=True)
#user_cod = db.Column(db.Integer, db.ForeignKey('user.id'))
#channel_cod = db.Column(db.Integer, db.ForeignKey('channel.id'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(length=30), nullable=False, unique=True)
    name = db.Column(db.String(length=30), nullable=False)
    last_name = db.Column(db.String(length=30), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)

    sex_id = db.Column(db.Integer, db.ForeignKey('sex.id'))
    sex = db.relationship("Sex", back_populates="users")

    email = db.Column(
        db.String, nullable=False, unique=True)
    password = db.Column(db.String(length=12), nullable=False)

    user_channel = db.relationship(
        'Channel', back_populates='owner', uselist=False)
    subcribed_to = db.relationship(
        'Channel', secondary=relation_subscriber, back_populates='subscriptions', lazy='dynamic')
#    rel_play_user = db.relationship(
#        'RelationUserPlay', back_populates='user_playlist', lazy=True)


class Sex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sex_name = db.Column(db.String(length=30), nullable=False)
    users = db.relationship('User', back_populates='sex', lazy=True)


class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(length=30),
                             nullable=False, unique=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', back_populates='user_channel')

    creation_date = db.Column(db.DateTime, nullable=False)
#    video = db.relationship('Video', back_populates='owned_channel', uselist=False)
    subscriptions = db.relationship(
        'User', secondary=relation_subscriber, back_populates='subcribed_to', lazy='dynamic')


# class Playlist(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    playlist_name = db.Column(
#        db.String(length=30), nullable=False, unique=True)
#    playlist_video = db.relationship(
#        'RelationPlayVid', back_populates='playlist_videos', uselist=False)
#    playlist_user = db.relationship(
#        'RelationUserPlay', back_populates='playlist_from_user', uselist=False)


# class Video(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    video_title = db.Column(db.String(length=30), nullable=False)
#    release_date = db.Column(db.String(length=30), nullable=False)
#    author_rights = db.Column(db.String(length=30), nullable=False)
#    details = db.Column(db.Integer, db.ForeignKey('details.id'))
#    channel_col = db.Column(db.Integer, db.ForeignKey('channel.id'))
#    videos_play = db.relationship(
#        'RelationPlayVid', back_populates='video_from_playlist', uselist=False)
#    details = db.relationship('Details', back_populates='owned_video', uselist=False)
#    channel = db.relationship('Channel', back_populates='video_from_channel', uselist=False)


# class Details(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    likes = db.Column(db.Integer)
#    dislikes = db.Column(db.Integer)
#    reproductions = db.Column(db.Integer)
#    video = db.relationship('Video', back_populates='owned_details', uselist=False)


# class RelationPlayVid(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    video_cod = db.Column(db.Integer, db.ForeignKey('video.id'))
#    playlist_cod = db.Column(db.Integer, db.ForeignKey('playlist.id'))
#    playlist_rel = db.relationship(
#        'Playlist', back_populates='playlist', uselist=False)
#    videos = db.relationship(
#        'Video', back_populates='video', uselist=False)


# class RelationUserPlay(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    user_cod = db.Column(db.Integer, db.ForeignKey('user.id'))
#    playlist_cod = db.Column(db.Integer, db.ForeignKey('playlist.id'))
#    users = db.relationship('User', back_populates='user_play', uselist=False)
#    playlist = db.relationship(
#        'playlist', back_populates='playlist_from_user', uselist=False)
