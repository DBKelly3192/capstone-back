from flask_login import UserMixin
from peewee import *
from playhouse.db_url import connect
import datetime
import os

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = SqliteDatabase('happy_trails.sqlite')

class BaseModel(Model):
    time = DateTimeField(default = datetime.datetime.now)

    class Meta:
        database = DATABASE

class User(BaseModel, UserMixin):
    email = CharField(unique = True)
    emergencyEmail = CharField()
    emergencyFirst = CharField()
    emergencyLast = CharField()
    first = CharField()
    last = CharField()
    lat = CharField()
    lng = CharField()
    password = CharField()
    photo = CharField()
    username = CharField(unique = True)

class Post(BaseModel):
    activity = CharField()
    description = CharField()
    location = CharField()
    user = ForeignKeyField(User, backref = 'posts')

class Sos(BaseModel):
    activity = CharField()
    description = CharField()
    finish = CharField()
    location = CharField()
    start = CharField()
    user = ForeignKeyField(User, backref = 'soss')

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post, Sos], safe = True)
    print("TABLES CREATED")
    DATABASE.close()
