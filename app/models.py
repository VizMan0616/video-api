from datetime import datetime as dt
from passlib.hash import pbkdf2_sha256 as sha256
from . import db
from sqlalchemy.sql.expression import func

relation_subscriber = db.Table('relationsubscriber', db.Model.metadata, db.Column(
    'user_id', db.Integer, db.ForeignKey('user.id')), db.Column('channel_id', db.Integer, db.ForeignKey('channel.id')))

relation_playlist_user = db.Table('relationplayuser', db.Model.metadata, db.Column(
    'user_id', db.Integer, db.ForeignKey('user.id')), db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')))

relation_playlist_video = db.Table('relationplayvideo', db.Model.metadata, db.Column(
    'video_id', db.Integer, db.ForeignKey('video.id')), db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(length=30), nullable=False, unique=True)
    first_name = db.Column(db.String(length=30), nullable=False)
    last_name = db.Column(db.String(length=30), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)

    sex_id = db.Column(db.Integer, db.ForeignKey('sex.id'))
    sex = db.relationship("Sex", back_populates="users")

    email = db.Column(
        db.String, nullable=False, unique=True)
    password = db.Column(db.String(length=87), nullable=False)

    user_channel = db.relationship(
        'Channel', back_populates='owner', uselist=False)
    subcribed_to = db.relationship(
        'Channel', secondary=relation_subscriber, back_populates='subscriptions', lazy='dynamic')
    playlists = db.relationship('Playlist', secondary=relation_playlist_user,
                                back_populates='playlists_of', lazy='dynamic')

    def __init__(self, username, first_name, last_name, birth_date, sex_id, email, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex_id = sex_id
        self.email = email
        self.password = sha256.hash(password)

    @classmethod
    def get_users(self):
        return self.query.all()

    @classmethod
    def get_user_id(self, user_id):
        return self.query.filter_by(id=user_id).first()

    @classmethod
    def get_user_username(self, username):
        return self.query.filter_by(username=username).first()

    @classmethod
    def get_user_email(self, email):
        return self.query.filter_by(email=email).first()

    def set_subscription(self, channel):
        self.subcribed_to.append(channel)

    def verify_password(self, str_password):
        return sha256.verify(str_password, self.password)


class Sex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sex_name = db.Column(db.String(length=30), nullable=False)
    users = db.relationship('User', back_populates='sex', lazy=True)

    def __init__(self, sex_name):
        self.sex_name = sex_name

    @classmethod
    def get_sex(self):
        return self.query.all()

    @classmethod
    def get_sex_id(self, sex_id):
        return self.query.filter_by(id=sex_id).first()


class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(length=30),
                             nullable=False, unique=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', back_populates='user_channel')

    creation_date = db.Column(db.DateTime, default=dt.utcnow())
    videos = db.relationship(
        'Video', back_populates='video_of', lazy=True)
    subscriptions = db.relationship(
        'User', secondary=relation_subscriber, back_populates='subcribed_to', lazy='dynamic')

    def __init__(self, channel_name, owner_id):
        self.channel_name = channel_name
        self.owner_id = owner_id

    @classmethod
    def get_channels(self):
        return self.query.all()

    @classmethod
    def get_channel_id(self, id):
        return self.query.filter_by(id=id).first()

    @classmethod
    def get_channel_name(self, channel_name):
        return self.query.filter_by(channel_name=channel_name).first()


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_name = db.Column(db.String(length=30), nullable=False)
    playlists_of = db.relationship(
        'User', secondary=relation_playlist_user, back_populates='playlists', lazy='dynamic')
    videos = db.relationship('Video', secondary=relation_playlist_video,
                             back_populates='playlist_in', lazy='dynamic')

    def __init__(self, playlist_name):
        self.playlist_name = playlist_name


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_title = db.Column(db.String(length=255), nullable=False)
    release_date = db.Column(db.DateTime, default=dt.utcnow())
    description = db.Column(db.String(length=500))
    details = db.relationship(
        'Details', back_populates='video', uselist=False, cascade="all, delete, delete-orphan")

    video_of_id = db.Column(db.Integer, db.ForeignKey('channel.id'))
    video_of = db.relationship(
        'Channel', back_populates='videos')
    playlist_in = db.relationship(
        'Playlist', secondary=relation_playlist_video, back_populates='videos', lazy='dynamic')

    def __init__(self, video_title, channel_id, description=''):
        self.video_title = video_title
        self.description = description
        self.video_of_id = channel_id

    @classmethod
    def get_videos(self):
        return self.query.all()

    @classmethod
    def get_videos(self):
        return self.query.all()

    @classmethod
    def get_random_videos_order(self):
        return self.query.order_by(func.random()).all()

    @classmethod
    def get_video_id(self, video_id):
        return self.query.filter_by(id=video_id).first()

    @classmethod
    def get_matched_videos(self, match_name):
        return self.query.filter(self.video_title.like(f'%{match_name}%')).all()


class Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer, default=0)
    reproductions = db.Column(db.Integer, default=0)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    video = db.relationship('Video', back_populates='details')

    def __init__(self, video_id):
        self.likes = 0
        self.reproductions = 0
        self.video_id = video_id

    def like(self):
        self.likes += 1

    def unlike(self):
        self.likes -= 1

    def reproduced(self):
        self.reproductions += 1
